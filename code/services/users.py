from code.models import Interest, User


class UserService:
    @classmethod
    async def get_users(cls, page: int, size: int):
        users = await User.all().offset((page - 1) * size).limit(size).prefetch_related('interests')
        return users

    @classmethod
    async def get_user(cls, user_id):
        user = await User.filter(id=user_id).prefetch_related('interests').first()
        return user

    @classmethod
    async def update_user(cls, user_id, payload):
        user = await User.filter(id=user_id).prefetch_related('interests').first()

        interests = payload.pop('interests', [])

        for key, value in payload.items():
            if value:
                setattr(user, key, value)

        if interests:
            await user.interests.clear()
            interests = await Interest.filter(id__in=interests)
            await user.interests.add(*interests)

        await user.save()

        user = await User.filter(id=user_id).prefetch_related('interests').first()

        return user
