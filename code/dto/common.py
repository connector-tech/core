from typing import Generic, TypeVar

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel


Model = TypeVar('Model')


class ErrorResponse(BaseModel):
    message: str = Field(...)


class PaginatedResponse(GenericModel, Generic[Model]):
    count: int = Field(...)
    items: list[Model] = Field(...)
