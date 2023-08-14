from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.constants import SECRET_KEY, JWT_ALGORITHM


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def check_authentication(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=JWT_ALGORITHM)
        user_id = int(payload.get("sub"))

        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return payload
