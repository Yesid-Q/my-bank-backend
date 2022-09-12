from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from tortoise.exceptions import IntegrityError

from src.models.user_model import UserModel
from src.schemas.token_schema import TokenResponse
from src.schemas.auth_schema import LoginSchema, RegisterRequest
from src.utils.token_util import create_access_token, refresh_token
from src.utils.password_util import verify_password, get_password

auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@auth_router.post(
    '/login',
    name='Login.',
    status_code=status.HTTP_200_OK,
    response_model=TokenResponse
)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await UserModel.get_or_none(doc_number=form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return create_access_token({'sub': str(user.id)})


@auth_router.post(
    '/register',
    name='Register new user',   
    status_code=status.HTTP_201_CREATED,
    response_model=TokenResponse
)
async def register_user(auth_request: RegisterRequest):
    auth_request.password = get_password(auth_request.password)
    try:
        user = await UserModel.create(**auth_request.dict(exclude={'verify_password'}))
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f'{e}')
    
    return create_access_token({'sub': str(user.id)})


@auth_router.get(
    '/refresh',
    name='Register new user',   
    status_code=status.HTTP_201_CREATED,
    response_model=TokenResponse
)
async def register_user(auth_request: UserModel = Depends(refresh_token)):
    return create_access_token({'sub': str(auth_request.id)})