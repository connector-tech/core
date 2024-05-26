from pydantic import BaseModel


class UserQuestionnaireBaseRequest(BaseModel):
    question_id: str
    answer: str
