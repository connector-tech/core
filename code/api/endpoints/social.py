from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import JSONResponse

from code.api.deps import get_current_user_id
from code.dto.common import PaginatedResponse
from code.dto.social import LikeUserBaseRequest
from code.dto.users import UserListBaseResponse
from code.models import UserLike


router = APIRouter(prefix='/social', tags=['social'])


@router.post('/like/')
async def like_user(payload: LikeUserBaseRequest, user_id: str = Depends(get_current_user_id)):
    await UserLike.create(user_id=user_id, liked_user_id=payload.user_id)
    return Response(status_code=status.HTTP_201_CREATED)


@router.get('/matches/', response_model=PaginatedResponse[UserListBaseResponse])
async def get_matches(user_id: str = Depends(get_current_user_id)):
    user_ids = await UserLike.filter(liked_user_id=user_id).values_list('user_id', flat=True)
    matches = await UserLike.filter(user_id=user_id, liked_user_id__in=user_ids).prefetch_related('liked_user')

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'count': len(matches),
            'items': [
                {
                    'id': str(match.liked_user.id),
                    'username': match.liked_user.username,
                    'full_name': match.liked_user.full_name,
                    'email': match.liked_user.email,
                    'age': match.liked_user.age,
                    'bio': match.liked_user.bio,
                    'interests': [interest.name for interest in match.liked_user.interests],
                }
                for match in matches
            ],
        },
    )
