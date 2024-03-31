from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool = True
    database_url: PostgresDsn


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
