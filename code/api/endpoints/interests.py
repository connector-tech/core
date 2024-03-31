from fastapi import APIRouter
from loguru import logger
from starlette.responses import JSONResponse

from code.dto.interests import InterestsBaseResponse
from code.services.interests import get_interests


router = APIRouter(prefix='/interests', tags=['interests'])


@router.get('/', response_model=InterestsBaseResponse)
async def get_interests_handler():
    interests = await get_interests()
    logger.info(f'Interests: {interests}')
    return JSONResponse(
        content={
            'interests': interests,
        },
    )
