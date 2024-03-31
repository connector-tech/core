from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise

from code.api import setup_routers
from code.config import settings, TORTOISE_CONFIG
from code.handlers import health


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await Tortoise.init(config=TORTOISE_CONFIG)
        yield
    finally:
        await Tortoise.close_connections()


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.add_api_route('/health/', health)
setup_routers(app)

if __name__ == '__main__':
    uvicorn.run('code.app:app', host='0.0.0.0', reload=settings.debug)
