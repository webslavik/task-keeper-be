from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.user import User


async def test_register_user(client: AsyncClient, db: AsyncSession, base_user):
    response = await client.post("/api/auth/register", json=base_user)

    assert response.status_code == 201
    assert response.json() == None

    stmt = select(User).where(User.email == base_user["email"])
    result = await db.scalars(stmt)

    assert result.one_or_none() is not None


async def test_login_user(client: AsyncClient, base_user):
    response = await client.post("/api/auth/login", json={
        "email": base_user["email"],
        "password": base_user["password"]
    })

    assert response.status_code == 200
    assert isinstance(response.json()['access_token'], str)
    assert 'password' not in response.json()['user']
