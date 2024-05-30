from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user_similarity" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "similarity" DOUBLE PRECISION NOT NULL,
    "user_1_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    "user_2_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_user_simila_user_1__60e9e4" UNIQUE ("user_1_id", "user_2_id")
);
CREATE INDEX IF NOT EXISTS "idx_user_simila_user_1__60e9e4" ON "user_similarity" ("user_1_id", "user_2_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "user_similarity";"""
