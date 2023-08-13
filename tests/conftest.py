import pytest

import asyncio
from httpx import AsyncClient

from src.main import app
from src.db_setup import Base, engine, async_session


@pytest.fixture()
def base_user():
    return {
        "email": "test_user_1@g.com",
        "password": "test_user_12344",
        "first_name": 'Jack',
        "last_name": 'Jackson'
    }


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope='session')
async def db():
    session = async_session()
    try:
        yield session
    finally:
        await session.close()
