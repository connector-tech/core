import datetime

from pydantic import BaseModel


class ChatListBaseResponse(BaseModel):
    class Receiver(BaseModel):
        id: str  # noqa
        username: str
        avatar: str

    id: str  # noqa
    receiver: Receiver
    last_message: str | None
    is_read: bool


class MessageListBaseResponse(BaseModel):
    id: str  # noqa
    text: str
    created_at: datetime.datetime
    is_me: bool
