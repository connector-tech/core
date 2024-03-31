from pydantic import BaseModel, Field


class SignInBaseRequest(BaseModel):
    email: str = Field(...)
    password: str = Field(...)


class SignUpBaseRequest(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)
    confirm_password: str = Field(...)


class SignUpBaseResponse(BaseModel):
    full_name: str = Field(...)
    email: str = Field(...)
    age: int = Field(...)
    created_at: str = Field(...)
