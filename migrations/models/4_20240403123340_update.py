from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" ADD "birth_date" DATE;
        ALTER TABLE "users" DROP COLUMN "age";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" ADD "age" INT;
        ALTER TABLE "users" DROP COLUMN "birth_date";"""
