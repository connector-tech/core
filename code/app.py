import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from code.config import settings
from code.handlers import health


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.add_api_route('/health/', health)

if __name__ == '__main__':
    uvicorn.run('code.app:app', host='0.0.0.0', reload=settings.debug)
