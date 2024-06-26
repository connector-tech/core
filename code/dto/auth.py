import datetime

from pydantic import BaseModel, Field

from code.models import User


class SignInBaseRequest(BaseModel):
    email: str = Field(...)
    password: str = Field(...)


class SignInBaseResponse(BaseModel):
    access_token: str = Field(...)


class SignUpBaseRequest(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    email: str = Field(...)
    birth_date: datetime.date = Field(...)
    bio: str = Field(...)
    gender: User.GenderEnum = Field(...)
    interests: list[str] = Field(default=[])
    password: str = Field(...)
    confirm_password: str = Field(...)
