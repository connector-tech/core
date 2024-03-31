from pydantic import BaseModel, Field


class InterestBaseItem(BaseModel):
    id: str = Field(default=None)  # noqa
    name: str = Field(default=None)


class InterestsBaseResponse(BaseModel):
    interests: list[InterestBaseItem] = Field(default=[])
