from datetime import datetime, timedelta, timezone

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from jose import jwt, JWTError

from src.configs.settings import settings
from src.configs.token_config import oauth2_scheme
from src.models.user_model import UserModel


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.TOKEN_ALGORITHM)
    return {
            'access_token': encoded_jwt,
            'token_type': 'Bearer'
        } 


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserModel:
    exception_credentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.TOKEN_ALGORITHM]
        )
        user_id: str = payload.get('sub')
        if user_id is None:
            raise exception_credentials
    except:
        raise exception_credentials

    user = await UserModel.get_or_none(pk=user_id)

    if user is None:
        raise exception_credentials

    if user.deleted_at is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Inactice user.')

    return user


async def refresh_token(token: str = Depends(oauth2_scheme)) -> UserModel:
    exception_credentials = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='Not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            leeway=30000,
            algorithms=[settings.TOKEN_ALGORITHM]
        )
        print(payload)
        user_id: str = payload.get('sub')
        if user_id is None:
            raise exception_credentials
    except:
        raise exception_credentials

    user = await UserModel.get_or_none(pk=user_id)

    if user is None:
        raise exception_credentials

    if user.deleted_at is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Inactice user.')

    return user
