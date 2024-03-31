from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" RENAME COLUMN "full_name" TO "first_name";
        ALTER TABLE "users" ADD "last_name" VARCHAR(255) NOT NULL;
        ALTER TABLE "users" ALTER COLUMN "username" DROP NOT NULL;
        ALTER TABLE "users" ALTER COLUMN "age" DROP NOT NULL;
        CREATE UNIQUE INDEX "uid_users_email_133a6f" ON "users" ("email");
        CREATE UNIQUE INDEX "uid_users_usernam_266d85" ON "users" ("username");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX "idx_users_usernam_266d85";
        DROP INDEX "idx_users_email_133a6f";
        ALTER TABLE "users" RENAME COLUMN "first_name" TO "full_name";
        ALTER TABLE "users" ADD "full_name" VARCHAR(255) NOT NULL;
        ALTER TABLE "users" DROP COLUMN "last_name";
        ALTER TABLE "users" ALTER COLUMN "username" SET NOT NULL;
        ALTER TABLE "users" ALTER COLUMN "age" SET NOT NULL;"""
