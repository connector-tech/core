from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "interests" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(255) NOT NULL UNIQUE
);
    ALTER TABLE "users" ADD "bio" TEXT;
        CREATE TABLE "user_interests" (
    "users_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    "interest_id" UUID NOT NULL REFERENCES "interests" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" DROP COLUMN "bio";
        DROP TABLE IF EXISTS "user_interests";
        DROP TABLE IF EXISTS "interests";"""
