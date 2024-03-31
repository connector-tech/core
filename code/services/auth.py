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


async def login(data: dict) -> User:
    user = await User.get(email=data['email'])
    if not user:
        raise ValueError('User not found')

    if not user.check_password(data['password']):
        raise ValueError('Invalid password')

    return user
