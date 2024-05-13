import asyncio

from datetime import datetime, timezone, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from tortoise import Tortoise
from tortoise.expressions import Q
from tortoise.transactions import in_transaction

from code.config import TORTOISE_CONFIG
from code.models import Chat, Message

scheduler = AsyncIOScheduler(timezone='UTC')


async def update_chat_last_message():
    now = datetime.now(timezone.utc)
    start_time = now - timedelta(hours=24)

    async with in_transaction():
        chats = await Chat.filter(
            Q(last_message__lt=start_time)
            | Q(last_message__isnull=True)
        ).all()

        for chat in chats:
            last_message_time = await Message.filter(
                chat_id=chat.id
            ).order_by('-created_at').first().only('created_at')
            chat.last_message = last_message_time.created_at
        await Chat.bulk_update(chats, ['last_message'])


scheduler.add_job(
    update_chat_last_message,
    trigger='interval',
    hours=24,
    next_run_time=datetime.now(timezone.utc),
)


async def main():
    await Tortoise.init(config=TORTOISE_CONFIG)

    scheduler.start()
    await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())
