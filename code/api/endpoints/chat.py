import asyncio
import uuid

from fastapi import APIRouter, Depends, Query, status, WebSocket
from fastapi.responses import JSONResponse
from loguru import logger

from code.api.deps import get_current_user_id
from code.dto.chat import ChatListBaseResponse, MessageListBaseResponse, ChatCreateBaseResponse, ChatCreateBaseRequest
from code.dto.common import PaginatedResponse, ErrorResponse
from code.models import Chat, Message
from code.services.chat import ChatService

router = APIRouter(prefix='/chats', tags=['chats'])

connected_users = {}


@router.get(
    '/',

    responses={
        200: {'model': PaginatedResponse[ChatListBaseResponse]},
        400: {'model': ErrorResponse},
        500: {'model': ErrorResponse},
    },
)
async def get_chats_handler(
    user_id: str = Depends(get_current_user_id),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=10, le=100, default=10),
):
    try:
        chats = await ChatService.get_chats(user_id, page=page, size=size)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={'message': f'Error: {e}'},
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'count': len(chats),
            'items': [
                {
                    'id': str(chat.id),
                    'receiver': chat.receiver,
                    'last_message': chat.last_message,
                    'is_read': chat.is_read,
                }
                for chat in chats
            ],
        },
    )


@router.post(
    '/',
    responses={
        201: {'model': ChatCreateBaseResponse},
        400: {'model': ErrorResponse},
        500: {'model': ErrorResponse},
    },
)
async def create_chat_handler(
    data: ChatCreateBaseRequest,
    user_id: str = Depends(get_current_user_id),
):
    try:
        chat_id = str(uuid.uuid4())
        await Chat.create(
            id=chat_id,
            user_1_id=user_id,
            user_2_id=data.receiver_id,
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={'message': f'Error: {e}'},
        )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            'id': chat_id,
        },
    )


@router.get(
    '/{chat_id}/messages/',
    responses={
        200: {'model': PaginatedResponse[MessageListBaseResponse]},
        400: {'model': ErrorResponse},
        500: {'model': ErrorResponse},
    },
)
async def get_messages_handler(
    chat_id: str,
    user_id: str = Depends(get_current_user_id),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=10, le=100, default=10),
):
    try:
        messages = await ChatService.get_messages(user_id, chat_id, page=page, size=size)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={'message': f'Error: {e}'},
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'count': len(messages),
            'items': [
                {
                    'id': str(message.id),
                    'text': message.text,
                    'created_at': str(message.created_at),
                    'is_me': message.is_me,
                }
                for message in messages
            ],
        },
    )


async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()

    connected_users[user_id] = websocket
    logger.info(f'websocket connected: {user_id}')

    try:
        while True:
            data = await websocket.receive_json()
            logger.info(f'websocket data: {data}')

            receiver_id = data.get('receiver_id')
            receiver = connected_users.get(receiver_id)

            coros = [
                asyncio.create_task(
                    Message.create(
                        user_id=user_id,
                        chat_id=data['chat_id'],
                        text=data['text'],
                    ),
                )
            ]

            if receiver:
                coros.append(asyncio.create_task(receiver.send_json(data)))
            responses = await asyncio.gather(*coros, return_exceptions=True)

            logger.info(f'coro responses: {responses}')

            for response in responses:
                if isinstance(response, Exception):
                    logger.error(f'websocket error: {response}')
    except Exception as e:
        logger.error(f'websocket error: {e}')
        connected_users.pop(user_id, None)
        await websocket.close()
