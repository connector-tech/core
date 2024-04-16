from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "chats" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "user_1_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    "user_2_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_chats_user_1__7bf97f" UNIQUE ("user_1_id", "user_2_id")
);
CREATE INDEX IF NOT EXISTS "idx_chats_user_1__0900e4" ON "chats" ("user_1_id", "user_2_id", "created_at");
        CREATE TABLE IF NOT EXISTS "messages" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "text" TEXT NOT NULL,
    "is_read" BOOL NOT NULL  DEFAULT False,
    "chat_id" UUID NOT NULL REFERENCES "chats" ("id") ON DELETE CASCADE,
    "user_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_messages_user_id_45cdaf" ON "messages" ("user_id", "created_at");
        CREATE UNIQUE INDEX "uid_user_social_viewer__99a131" ON "user_social" ("viewer_id", "user_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX "uid_user_social_viewer__99a131";
        DROP TABLE IF EXISTS "chats";
        DROP TABLE IF EXISTS "messages";"""
