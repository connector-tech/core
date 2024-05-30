from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX "idx_user_simila_user_1__60e9e4";
        CREATE INDEX "idx_user_simila_similar_0ab472" ON "user_similarity" ("similarity");
        CREATE INDEX "idx_user_simila_user_1__c782ad" ON "user_similarity" ("user_1_id");
        CREATE INDEX "idx_user_simila_user_2__58d762" ON "user_similarity" ("user_2_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX "idx_user_simila_user_2__58d762";
        DROP INDEX "idx_user_simila_user_1__c782ad";
        DROP INDEX "idx_user_simila_similar_0ab472";
        CREATE INDEX "idx_user_simila_user_1__60e9e4" ON "user_similarity" ("user_1_id", "user_2_id");"""
