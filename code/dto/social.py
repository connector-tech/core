from pydantic import BaseModel


class LikeUserBaseRequest(BaseModel):
    user_id: str
