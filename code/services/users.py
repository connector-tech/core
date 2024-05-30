from loguru import logger

from code.models import Interest, User, UserSocial, UserSimilarity

PREFERRED_GENDER_MAPPER = {
    User.GenderEnum.MALE: User.GenderEnum.FEMALE.value,
    User.GenderEnum.FEMALE: User.GenderEnum.MALE.value,
}


class UserService:
    @classmethod
    async def get_users(cls, viewer_id: str, page: int, size: int) -> list[User]:
        viewer = await User.filter(id=viewer_id).only('gender').first()
        viewed_user_ids = await UserSocial.filter(
            viewer_id=viewer_id,
        ).values_list('user_id', flat=True)

        users = (
            UserSimilarity.filter(user_1_id=viewer_id)
            .prefetch_related('user_2')
            .exclude(user_2_id__in=viewed_user_ids)
            .exclude(user_2_id=viewer_id)
            .filter(user_2__gender=PREFERRED_GENDER_MAPPER[viewer.gender])
            .order_by('-similarity')
            .offset((page - 1) * size)
            .limit(size)
            .prefetch_related('user_2__interests')  # noqa
        )
        logger.info(f'Users: {users.sql()}')
        users = await users
        users = [user.user_2 for user in users]
        logger.info(f'Users: {users}')

        for user in users:
            user.is_liked = await UserSocial.filter(
                viewer_id=user.id,
                user_id=viewer_id,
                is_liked=True,
            ).exists()

        return users

    @classmethod
    async def get_user(cls, user_id: str) -> User:
        user = await User.filter(id=user_id).prefetch_related('interests').first()
        return user

    @classmethod
    async def update_user(cls, user_id: str, payload: dict) -> User:
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
