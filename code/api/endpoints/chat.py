import asyncio
import uuid

from fastapi import APIRouter, Depends, Query, status, WebSocket
from fastapi.responses import JSONResponse
from loguru import logger
from tortoise.expressions import Q

from code.api.deps import get_current_user_id
from code.dto.chat import ChatListBaseResponse, MessageListBaseResponse, ChatCreateBaseResponse, ChatCreateBaseRequest
from code.dto.common import PaginatedResponse, ErrorResponse
from code.models import Chat, UserSocial
from code.services.chat import ChatService
from code.clients.websockets import WebSocketClient

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
        await asyncio.gather(
            Chat.create(
                id=chat_id,
                user_1_id=user_id,
                user_2_id=data.receiver_id,
            ),
            UserSocial.filter(
                Q(Q(viewer_id=user_id) & Q(user_id=data.receiver_id))
                | Q(Q(viewer_id=data.receiver_id) & Q(user_id=user_id))
            ).update(is_chat_started=True),
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
    await WebSocketClient.connect(user_id, websocket)

    async for message in websocket.iter_json():
        logger.info(f'message {user_id} sent to websocket: {message}')
        await WebSocketClient.send_personal_message(message, user_id)
    await WebSocketClient.disconnect(user_id)
