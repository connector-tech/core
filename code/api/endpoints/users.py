from fastapi import APIRouter, status
from starlette.responses import JSONResponse

from code.dto.users import UserDetailBaseResponse, UserUpdateBaseRequest
from code.services.users import UserService


router = APIRouter(prefix='/users', tags=['users'])


@router.get('/', response_model=UserDetailBaseResponse)
async def get_user_handler(user_id: str):
    try:
        user = await UserService.get_user(user_id)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'message': str(e)},
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'id': str(user.id),
            'username': user.username,
            'full_name': user.full_name,
            'email': user.email,
            'age': user.age,
            'bio': user.bio,
            'interests': [interest.name for interest in user.interests],
        },
    )


@router.put('/{user_id}', response_model=UserDetailBaseResponse)
async def update_user_handler(user_id: str, payload: UserUpdateBaseRequest):
    try:
        user = await UserService.update_user(user_id, payload.model_dump())
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'message': str(e)},
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'id': str(user.id),
            'username': user.username,
            'full_name': user.full_name,
            'email': user.email,
            'age': user.age,
            'bio': user.bio,
            'interests': [interest.name for interest in user.interests],
        },
    )
