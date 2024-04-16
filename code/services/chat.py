from tortoise.expressions import Case, Q, When

from code.models import Chat, Message


class ChatService:
    @classmethod
    async def get_messages(cls, user_id: str, chat_id: str, page: int, size: int) -> list[Message]:
        messages = (
            await Message.filter(
                chat_id=chat_id,
            )
            .order_by(
                '-created_at',
            )
            .offset((page - 1) * size)
            .limit(size)
            .annotate(
                is_me=Case(
                    When(user_id=user_id, then=True),
                    default=False,
                ),
            )
        )

        for message in messages:
            if not message.is_me and not message.is_read:
                message.is_read = True
                await message.save(update_fields=['is_read'])

        return messages

    @classmethod
    async def get_chats(cls, user_id: str, page: int, size: int) -> list[Chat]:
        chats = (
            await Chat.filter(
                Q(user1_id=user_id) | Q(user2_id=user_id),
            )
            .order_by('-created_at')
            .offset((page - 1) * size)
            .limit(size)
        )

        for chat in chats:
            last_message = (
                await Message.filter(
                    chat_id=chat.id,
                )
                .exclude(
                    user_id=user_id,
                )
                .order_by('-created_at')
                .first()
            )
            chat.last_message = last_message.text if last_message else None
            chat.is_read = last_message.is_read if last_message else True
        return chats
