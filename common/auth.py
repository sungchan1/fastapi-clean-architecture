from datetime import timedelta, datetime, UTC

from fastapi import HTTPException, status
from jose import jwt, JWTError

SECRET_KEY = "THIS_IS_SUPER_SECRET_KEY"
ALGORITHM = "HS256"

def create_access_token(
        payload: dict,
        expires_delta: timedelta = timedelta(hours=6)
):
    expire = datetime.now(UTC) + expires_delta
    payload.update({"exp" :expire})
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def decode_access_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status=status.HTTP_401_UNAUTHORIZED)


