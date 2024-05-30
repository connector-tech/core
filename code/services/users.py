from code.models import Interest, User, UserSocial

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

        users = await (
            User.exclude(id__in=viewed_user_ids)
            .exclude(id=viewer_id)
            .filter(gender=PREFERRED_GENDER_MAPPER[viewer.gender])
            .order_by('-created_at')
            .offset((page - 1) * size)
            .limit(size)
            .prefetch_related('interests')  # noqa
        )

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
