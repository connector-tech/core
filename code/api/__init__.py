from fastapi import FastAPI

from code.api.endpoints import auth, health, interests, users


def setup_routers(app: FastAPI):
    app.include_router(health.router)
    app.include_router(auth.router)
    app.include_router(interests.router)
    app.include_router(users.router)
