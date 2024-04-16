from fastapi import APIRouter, Depends, Query, status, UploadFile
from starlette.responses import JSONResponse

from code.api.deps import get_current_user_id
from code.dto.common import PaginatedResponse
from code.dto.users import (
    UploadUserPhotosBaseResponse,
    UserDetailBaseResponse,
    UserListBaseResponse,
    UserUpdateBaseRequest,
)
from code.services.media import MediaService
from code.services.users import UserService


router = APIRouter(prefix='/users', tags=['users'])


@router.get('/', response_model=PaginatedResponse[UserListBaseResponse])
async def get_users_handler(
    user_id: str = Depends(get_current_user_id),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=10, le=100, default=10),
):
    users = await UserService.get_users(
        viewer_id=user_id,
        page=page,
        size=size,
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'count': len(users),
            'items': [
                {
                    'id': str(user.id),
                    'username': user.username,
                    'full_name': user.full_name,
                    'email': user.email,
                    'age': user.age,
                    'bio': user.bio,
                    'is_liked': user.is_liked,
                    'photos': user.photos,
                    'gender': user.gender,
                    'interests': [interest.name for interest in user.interests],
                }
                for user in users
            ],
        },
    )


@router.put('/', response_model=UserDetailBaseResponse)
async def update_user_handler(payload: UserUpdateBaseRequest, user_id: str = Depends(get_current_user_id)):
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
            'photos': user.photos,
            'interests': [interest.name for interest in user.interests],
        },
    )


@router.get('/me/', response_model=UserDetailBaseResponse)
async def get_my_user_handler(user_id: str = Depends(get_current_user_id)):
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
            'photos': user.photos,
            'gender': user.gender,
            'interests': [interest.name for interest in user.interests],
        },
    )


@router.post('/photos/upload/', response_model=UploadUserPhotosBaseResponse)
async def upload_user_photos_handler(photos: list[UploadFile], user_id: str = Depends(get_current_user_id)):
    try:
        uploaded_photo_ids = await MediaService.upload_user_photos(user_id, photos)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'message': str(e)},
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content={'photos': uploaded_photo_ids})
