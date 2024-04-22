from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool = True
    database_url: PostgresDsn
    secret_key: str = 'secret'
    jwt_expire: int = 24 * 60 * 60
    jwt_algorithm: str = 'HS256'
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_bucket_name: str


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
