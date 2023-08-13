from sys import modules

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from src.constants import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, DB_USER_TEST, DB_PASSWORD_TEST, DB_HOST_TEST, DB_NAME_TEST


db_url = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

if "pytest" in modules:
    db_url = f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASSWORD_TEST}@{DB_HOST_TEST}/{DB_NAME_TEST}"


engine = create_async_engine(
    db_url,
    future=True,
    echo=False
)
async_session = async_sessionmaker(engine)

class Base(DeclarativeBase):
    pass

async def get_db():
    db: AsyncSession = async_session()
    try:
        yield db
    finally:
        await db.close()
