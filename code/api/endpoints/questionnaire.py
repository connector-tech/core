from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from code.api.deps import get_current_user_id
from code.dto.questionnaire import UserQuestionnaireBaseRequest
from code.models import UserQuestionnaireAnswer, QuestionnaireQuestion

router = APIRouter(prefix='/questionnaire', tags=['questionnaire'])


@router.get('/questions/')
async def get_questionnaire_questions_handler():
    questions = await QuestionnaireQuestion.all()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=[
            {
                'id': str(question.id),
                'question': question.text,
            } for question in questions
        ]
    )


@router.post('/')
async def save_user_answers_for_questionnaire_handler(
    payload: list[UserQuestionnaireBaseRequest],
    user_id: str = Depends(get_current_user_id)
):
    try:
        answers = [UserQuestionnaireAnswer(user_id=user_id, **(answer.model_dump())) for answer in payload]
        await UserQuestionnaireAnswer.bulk_create(answers)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'message': str(e)},
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content={})
