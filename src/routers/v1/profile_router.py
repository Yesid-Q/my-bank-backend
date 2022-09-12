from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from src.models.user_model import UserModel
from src.models.account_model import AccountModel
from src.utils.token_util import get_current_user
from src.utils.password_util import verify_password
from src.schemas.user_schema import UserResponse
from src.schemas.account_schema import AccountResponse
from src.schemas.profile_schema import ProfileRequest, PasswordRequest


profile_router = APIRouter(
    prefix='/profile',
    tags=['profile']
)

@profile_router.get(
    '',
    name='Profile info.',
    status_code=status.HTTP_200_OK,
    response_model=UserResponse
)
async def info_profile(current_user: UserModel = Depends(get_current_user)):
    await current_user.fetch_related('document')
    return current_user


@profile_router.get(
    '/accounts',
    name='Profile Accounts.',
    status_code=status.HTTP_200_OK,
    response_model=List[AccountResponse]
)
async def get_account_profile(current_user: UserModel = Depends(get_current_user)):
    accounts = await AccountModel.filter(user_id=current_user.id).prefetch_related('type_account')
    return accounts


@profile_router.put(
    '',
    name='Update profile.',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=UserResponse
)
async def update_profile(
    profile_request: ProfileRequest,
    current_user: UserModel = Depends(get_current_user)
):
    await UserModel.filter(pk=current_user.id).update(**profile_request.dict(exclude_none=True))
    user = await UserModel.filter(pk=current_user.id).prefetch_related('document').first()
    return user


@profile_router.put(
    '/change/password',
    name='Update profile.',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=UserResponse
)
async def update_profile(
    password_request: PasswordRequest,
    current_user: UserModel = Depends(get_current_user)
):
    if not verify_password(password_request.old_password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    await UserModel.filter(pk=current_user.id).update(password=password_request.new_password)
    user = await UserModel.filter(pk=current_user.id).prefetch_related('document').first()
    return user


@profile_router.delete(
    '',
    name='Update profile.',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_profile(
    current_user: UserModel = Depends(get_current_user)
):
    values = await AccountModel.filter(user_id=current_user.id).values_list('amount', flat=True)
    for value in values:
        if value > 0:
            break
    else:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail={
                'error': 'The account has cash available',
                'values': values
            }
        )

    await current_user.delete()
    return

