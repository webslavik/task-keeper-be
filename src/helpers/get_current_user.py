from fastapi import Depends, HTTPException, status

from src.repositories.user import UserRepository
from src.db_setup import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from src.helpers import check_authentication


async def get_current_user(payload: int = Depends(check_authentication), db: AsyncSession = Depends(get_db)):
    user = await UserRepository.get_user_by_id(db, int(payload.get("sub")))

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user
