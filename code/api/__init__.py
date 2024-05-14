from fastapi import FastAPI

from code.api.endpoints import auth, chat, health, interests, social, users


def setup_routers(app: FastAPI):
    app.include_router(health.router)
    app.include_router(auth.router)
    app.include_router(interests.router)
    app.include_router(users.router)
    app.include_router(social.router)
    app.include_router(chat.router)
    app.add_api_websocket_route('/ws/{user_id}/', chat.websocket_endpoint)
