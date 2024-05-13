from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user_social" ADD "is_chat_started" BOOL NOT NULL  DEFAULT False;
    """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user_social" DROP COLUMN "is_chat_started";"""
