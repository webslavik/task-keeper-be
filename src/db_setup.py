from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from src.constants import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME


SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    future=True
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
