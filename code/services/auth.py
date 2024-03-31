from code.models import User
from code.utils import hash_password


async def register(data: dict) -> User:
    if data['password'] != data['confirm_password']:
        raise ValueError('Passwords do not match')

    hashed_password = hash_password(data['password'])

    user = await User.create(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password=hashed_password,
    )

    return user
