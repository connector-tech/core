from pydantic import BaseModel


class UserDetailBaseResponse(BaseModel):
    id: str  # noqa
    username: str
    full_name: str
    email: str
    age: int
    bio: str
    interests: list[str] = []


class UserUpdateBaseRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    age: int | None = None
    bio: str | None = None
    interests: list[str] = []


class UserListBaseResponse(BaseModel):
    id: str  # noqa
    username: str
    full_name: str
    email: str
    age: int
    bio: str
    interests: list[str] = []
