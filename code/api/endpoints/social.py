from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import JSONResponse

from code.api.deps import get_current_user_id
from code.dto.common import PaginatedResponse
from code.dto.social import UserViewedBaseRequest
from code.dto.users import UserListBaseResponse
from code.models import UserSocial


router = APIRouter(prefix='/social', tags=['social'])


@router.post('/viewed/')
async def viewed_user(payload: UserViewedBaseRequest, user_id: str = Depends(get_current_user_id)):
    await UserSocial.create(
        viewer_id=user_id,
        user_id=payload.user_id,
        is_liked=payload.is_liked,
    )
    return Response(status_code=status.HTTP_201_CREATED)


@router.get('/matches/', response_model=PaginatedResponse[UserListBaseResponse])
async def get_matches(user_id: str = Depends(get_current_user_id)):
    user_ids = await UserSocial.filter(
        user_id=user_id,
        is_liked=True,
    ).values_list('viewer_id', flat=True)

    matches = await UserSocial.filter(
        viewer_id=user_id,
        user_id__in=user_ids,
        is_liked=True,
        is_chat_started=False,
    ).prefetch_related('user', 'user__interests')

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'count': len(matches),
            'items': [
                {
                    'id': str(match.user.id),
                    'username': match.user.username,
                    'full_name': match.user.full_name,
                    'email': match.user.email,
                    'age': match.user.age,
                    'bio': match.user.bio,
                    'interests': [interest.name for interest in match.user.interests],
                }
                for match in matches
            ],
        },
    )
