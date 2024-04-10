from pydantic import BaseModel


class UserViewedBaseRequest(BaseModel):
    user_id: str
    is_liked: bool
