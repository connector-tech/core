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
        CREATE TABLE IF NOT EXISTS "user_interests" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "interest_id" UUID NOT NULL REFERENCES "interests" ("id") ON DELETE CASCADE,
    "user_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_user_intere_user_id_338e44" UNIQUE ("user_id", "interest_id")
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "user_interests";
        ALTER TABLE "users" DROP COLUMN "bio";
        DROP TABLE IF EXISTS "interests";
        DROP TABLE IF EXISTS "user_interests";"""
