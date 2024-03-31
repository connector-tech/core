from code.models import User, UserInterests
from code.utils import hash_password


async def register(data: dict) -> User:
    if data['password'] != data['confirm_password']:
        raise ValueError('Passwords do not match')

    hashed_password = hash_password(data['password'])

    interest_ids = data.pop('interests', [])

    user = await User.create(
        first_name=data['first_name'],
        last_name=data['last_name'],
        age=data['age'],
        bio=data['bio'],
        email=data['email'],
        password=hashed_password,
    )

    if interest_ids:
        await UserInterests.bulk_create(
            [UserInterests(user_id=user.id, interest_id=interest_id) for interest_id in interest_ids],
        )

    return user


async def login(data: dict) -> User:
    user = await User.get(email=data['email'])
    if not user:
        raise ValueError('User not found')

    if not user.check_password(data['password']):
        raise ValueError('Invalid password')

    return user
