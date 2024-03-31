from typing import AsyncGenerator

import pytest
from httpx import AsyncClient

from code.app import app


@pytest.fixture
async def client() -> AsyncGenerator:
    async with AsyncClient(app=app, base_url='http://test') as async_client:
        yield async_client
