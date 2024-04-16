from code.models import Interest, User
from code.utils import hash_password


async def register(data: dict) -> User:
    if data['password'] != data['confirm_password']:
        raise ValueError('Passwords do not match')

    hashed_password = hash_password(data['password'])

    interest_ids = data.pop('interests', [])

    user = await User.create(
        first_name=data['first_name'],
        last_name=data['last_name'],
        birth_date=data['birth_date'],
        gender=data['gender'],
        bio=data['bio'],
        email=data['email'],
        password=hashed_password,
    )

    if interest_ids:
        interests = await Interest.filter(id__in=interest_ids)
        await user.interests.add(*interests)

    return user


async def login(data: dict) -> User:
    user = await User.get(email=data['email'])
    if not user:
        raise ValueError('User not found')

    if not user.check_password(data['password']):
        raise ValueError('Invalid password')

    return user
