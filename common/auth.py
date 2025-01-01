from dataclasses import dataclass
from datetime import timedelta, datetime, UTC
from typing import Annotated

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from enum import StrEnum

from config import get_settings

settings = get_settings()

SECRET_KEY = settings.jwt_secret
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


class Role(StrEnum):
    ADMIN = "ADMIN"
    USER = "USER"


@dataclass
class CurrentUser:
    id: str
    role: Role

def create_access_token(
        payload: dict,
        role: Role,
        expires_delta: timedelta = timedelta(hours=6)
):
    expire = datetime.now(UTC) + expires_delta
    payload.update({"exp" :expire, "role": role})
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def decode_access_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)



def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = decode_access_token(token)
    user_id = payload.get("user_id")
    role = payload.get("role")
    if not user_id or not role or role != Role.USER:
        print(user_id, role)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return CurrentUser(user_id, Role(role))

def get_admin_user(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = decode_access_token(token)
    role = payload.get("role")
    if not role or role != Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return CurrentUser("ADMIN_USER_ID", role)

# todo admin 계정 관리 방법