from pydantic import BaseModel, Field


class SignInBaseRequest(BaseModel):
    email: str = Field(...)
    password: str = Field(...)


class SignInBaseResponse(BaseModel):
    access_token: str = Field(...)


class SignUpBaseRequest(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    email: str = Field(...)
    age: int = Field(...)
    bio: str = Field(...)
    interests: list[str] = Field(default=[])
    password: str = Field(...)
    confirm_password: str = Field(...)
