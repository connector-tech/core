from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool = True
    database_url: PostgresDsn
    secret_key: str = 'secret'
    jwt_expire: int = 24 * 60 * 60
    jwt_algorithm: str = 'HS256'
    s3_access_key_id: str | None = None
    s3_secret_access_key: str | None = None
    s3_bucket_name: str | None = None
    aws_region: str | None = None


settings = Settings()

TORTOISE_CONFIG = {
    'connections': {'default': str(settings.database_url)},
    'apps': {
        'models': {
            'models': ['code.models', 'aerich.models'],
            'default_connection': 'default',
        },
    },
}
