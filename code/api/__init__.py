from fastapi import FastAPI

from code.api import auth


def setup_routers(app: FastAPI):
    app.include_router(auth.router)
