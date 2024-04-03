from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user_likes" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "liked_user_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    "user_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_user_likes_user_id_517f21" ON "user_likes" ("user_id", "liked_user_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "user_likes";"""
