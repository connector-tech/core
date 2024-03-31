from datetime import datetime, timedelta

from jose import jwt
from loguru import logger
from passlib.context import CryptContext

from code.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict) -> str:
    expire = datetime.utcnow() + timedelta(seconds=settings.jwt_expire)
    data.update({'expire': expire.isoformat()})
    return jwt.encode(data, settings.secret_key, settings.jwt_algorithm)


def verify_token(token: str) -> tuple[bool, int | None]:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
        if any(key not in payload for key in ('user_id', 'expire')):
            return False, None
        if datetime.fromisoformat(payload['expire']) < datetime.utcnow():
            return False, None
    except jwt.JWTError as e:
        logger.info(f'Error while decoding token: {e}')
        return False, None
    return True, payload['user_id']
