from pydantic import BaseSettings


class Settings(BaseSettings):
    debug: bool = True


settings = Settings()
