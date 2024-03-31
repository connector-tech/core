from fastapi import Header, HTTPException

from code.utils import verify_token


async def get_current_user_id(token: str = Header('Authorization')):
    if not token:
        raise HTTPException(status_code=401, detail='Token is required')

    is_verified, user_id = verify_token(token)

    if not is_verified:
        raise HTTPException(status_code=401, detail='Invalid token')

    return user_id
