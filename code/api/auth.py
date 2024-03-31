from fastapi import APIRouter
from fastapi.responses import JSONResponse

from code.dto.auth import SignInBaseRequest, SignInBaseResponse, SignUpBaseRequest, SignUpBaseResponse
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
async def sign_in(body: SignInBaseRequest):
    try:
        user = await login(body.model_dump())
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={'message': str(e)},
        )
    return JSONResponse(
        status_code=200,
        content={
            'access_token': create_access_token({'user_id': str(user.id)}),
        },
    )


@router.post(
    '/sign-up/',
    responses={
        200: {'model': SignUpBaseResponse},
        400: {'model': ErrorResponse},
    },
)
async def sign_up(body: SignUpBaseRequest):
    try:
        user = await register(body.model_dump())
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={'message': str(e)},
        )

    return JSONResponse(
        status_code=201,
        content={
            'full_name': user.full_name,
            'email': user.email,
            'age': user.age,
            'created_at': user.created_at.isoformat(),
        },
    )
