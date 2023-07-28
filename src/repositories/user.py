from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.user import UserBase
from src.models.user import User


class UserRepository:
    @classmethod
    async def get_user_by_id(cls, db: AsyncSession, user_id: int) -> User:
        stmt = select(User).where(User.id == user_id)
        result = await db.scalars(stmt)
        user = result.one_or_none()

        return user


    @classmethod
    async def get_user_by_email(cls, db: AsyncSession, email: str) -> User:
        stmt = select(User).where(User.email == email)
        result = await db.scalars(stmt)
        user = result.one_or_none()

        return user


    @classmethod
    async def create_user(cls, db: AsyncSession, user: UserBase) -> User:
        created_user = User(**user.dict())

        db.add(created_user)
        await db.commit()
        await db.refresh(created_user)

        return created_user
