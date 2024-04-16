import datetime

from pydantic import BaseModel


class UserDetailBaseResponse(BaseModel):
    id: str  # noqa
    username: str
    full_name: str
    email: str
    age: int
    bio: str
    photos: list[str] = []
    interests: list[str] = []


class UserUpdateBaseRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    birth_date: datetime.date | None = None
    bio: str | None = None
    interests: list[str] = []


class UserListBaseResponse(BaseModel):
    id: str  # noqa
    username: str
    full_name: str
    email: str
    age: int
    bio: str
    is_liked: bool | None = None
    photos: list[str] = []
    interests: list[str] = []


class UploadUserPhotosBaseResponse(BaseModel):
    photos: list[str]
