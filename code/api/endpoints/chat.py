import asyncio
import uuid

from fastapi import APIRouter, Depends, Query, status, WebSocket
from fastapi.responses import JSONResponse
from loguru import logger

from code.api.deps import get_current_user_id
from code.dto.chat import ChatListBaseResponse, MessageListBaseResponse
from code.dto.common import PaginatedResponse
from code.models import Chat, Message
from code.services.chat import ChatService


router = APIRouter(prefix='/chats', tags=['chats'])

connected_users = {}


@router.get('/', response_model=PaginatedResponse[ChatListBaseResponse])
async def get_chats_handler(
    user_id: str = Depends(get_current_user_id),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=10, le=100, default=10),
):
    chats = await ChatService.get_chats(user_id, page=page, size=size)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'count': len(chats),
            'items': [
                {
                    'id': str(chat.id),
                    'receiver': {
                        'id': str(chat.user_1.id if chat.user_2.id == user_id else chat.user_2.id),
                        'username': chat.user_1.username if chat.user_2.id == user_id else chat.user_2.username,
                        'avatar': chat.user_1.photos[0] if chat.user_2.id == user_id else chat.user_2.photos[0],
                    },
                    'last_message': chat.last_message,
                    'is_read': chat.is_read,
                }
                for chat in chats
            ],
        },
    )


@router.get('/{chat_id}/messages/', response_model=PaginatedResponse[MessageListBaseResponse])
async def get_messages_handler(
    chat_id: str,
    user_id: str = Depends(get_current_user_id),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=10, le=100, default=10),
):
    messages = await ChatService.get_messages(user_id, chat_id, page=page, size=size)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'count': len(messages),
            'items': [
                {
                    'id': str(message.id),
                    'text': message.text,
                    'created_at': message.created_at,
                    'is_me': message.is_me,
                }
                for message in messages
            ],
        },
    )


@router.websocket('/ws/{user_id}')
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()

    connected_users[user_id] = websocket

    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f'websocket data: {data}')

            receiver_id = data.get('receiver_id')
            receiver = connected_users.get(receiver_id)

            coros = []

            if not data.get('chat_id'):
                chat_id = str(uuid.uuid4())
                data['chat_id'] = chat_id
                coros.append(
                    asyncio.create_task(
                        Chat.create(
                            id=chat_id,
                            user1_id=user_id,
                            user2_id=receiver_id,
                        ),
                    ),
                )
            coros.append(
                asyncio.create_task(
                    Message.create(
                        user_id=user_id,
                        chat_id=data['chat_id'],
                        text=data['text'],
                    ),
                ),
            )

            if receiver:
                coros.append(asyncio.create_task(receiver.send_json(data)))
            await asyncio.gather(*coros, return_exceptions=True)
    except Exception as e:
        logger.error(f'websocket error: {e}')
        await websocket.close()
