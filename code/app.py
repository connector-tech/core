import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from tortoise import Tortoise

from code.api import setup_routers
from code.clients.boto3 import S3
from code.config import settings, TORTOISE_CONFIG


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await asyncio.gather(
            Tortoise.init(config=TORTOISE_CONFIG),
            S3.connect(
                access_key_id=settings.aws_access_key_id,
                secret_access_key=settings.aws_secret_access_key,
                bucket_name=settings.aws_bucket_name,
            ),
        )
        yield
    finally:
        await asyncio.gather(
            S3.disconnect(),
            Tortoise.close_connections(),
        )


app = FastAPI(lifespan=lifespan)

app.mount('/media', StaticFiles(directory='media'), name='media')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

setup_routers(app)

if __name__ == '__main__':
    uvicorn.run('code.app:app', host='0.0.0.0', port=80, reload=settings.debug)
