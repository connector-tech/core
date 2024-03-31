from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    message: str = Field(...)
