import asyncio

from fastapi.websockets import WebSocket
from loguru import logger

from code.models import Message


class WebSocketClient:
    _connected_users = None

    @classmethod
    async def init(cls) -> None:
        cls._connected_users: dict[str, WebSocket] = {}

    @classmethod
    async def connect(cls, user_id: str, websocket: WebSocket) -> None:
        try:
            await websocket.accept()
            cls._connected_users[user_id] = websocket
            logger.info(f'websocket connected: {user_id}')
        except Exception as e:
            logger.info(f'ERROR while connecting websocket user {user_id}: {e}')

    @classmethod
    async def disconnect(cls, user_id: str) -> None:
        try:
            websocket = cls._connected_users.get(user_id)
            if websocket:
                await websocket.close()
            cls._connected_users.pop(user_id, None)
            logger.info(f'websocket user succesfully disconnected: {user_id}')
        except Exception as e:
            logger.info(f'ERROR while disconnecting websocket user {user_id}: {e}')

    @classmethod
    async def send_personal_message(cls, data: dict, user_id: str):
        receiver = cls._connected_users.get(user_id)
        if not receiver:
            logger.info(f'websocket user not connected: {user_id}')
            return

        coros = [
            Message.create(
                user_id=user_id,
                chat_id=data['chat_id'],
                text=data['text'],
            ),
            receiver.send_json(data)
        ]

        responses = await asyncio.gather(*coros, return_exceptions=True)
        logger.info(f'coro responses: {responses}')

        for response in responses:
            if response is Exception:
                logger.info(f'ERROR while sending personal message: {response}')
