from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from code.dto.auth import SignInBaseRequest, SignInBaseResponse, SignUpBaseRequest
from code.dto.common import ErrorResponse
from code.services.auth import login, register
from code.utils import create_access_token


router = APIRouter(prefix='/auth', tags=['auth'])


@router.post(
    '/sign-in/',
    responses={
        200: {'model': SignInBaseResponse},
        400: {'model': ErrorResponse},
    },
)
async def sign_in_handler(body: SignInBaseRequest):
    try:
        user = await login(body.model_dump())
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'message': str(e)},
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'access_token': create_access_token({'user_id': str(user.id)}),
        },
    )


@router.post(
    '/sign-up/',
    responses={
        200: {'model': SignInBaseResponse},
        400: {'model': ErrorResponse},
    },
)
async def sign_up_handler(body: SignUpBaseRequest):
    try:
        user = await register(body.model_dump())
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'message': str(e)},
        )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            'access_token': create_access_token({'user_id': str(user.id)}),
        },
    )
