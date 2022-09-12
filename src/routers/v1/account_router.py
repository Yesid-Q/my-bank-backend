from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from tortoise.exceptions import IntegrityError

from src.models.user_model import UserModel
from src.models.account_model import AccountModel
from src.schemas.account_schema import AccountRequest, AccountResponse, AmountRequest
from src.utils.token_util import get_current_user


account_router = APIRouter(
    prefix='/account',
    tags=['account']
)


@account_router.post(
    '',
    name='Create Account.',
    status_code=status.HTTP_201_CREATED,
    response_model=AccountResponse
)
async def create_account(
    account_request: AccountRequest,
    current_user: UserModel = Depends(get_current_user)
):
    try:
        account = await AccountModel.create(**account_request.dict(), user_id=current_user.id)
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f'{e}')
    
    await account.fetch_related('type_account')
    
    return account


@account_router.put(
    '/{id}',
    name='Update Account.',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=AccountResponse
)
async def update_create(
    id: UUID,
    account_request: AccountRequest,
    current_user: UserModel = Depends(get_current_user)
):
    check = await AccountModel.filter(pk=id, user_id=current_user.id).first()
    if check is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Account information does not match {id}.')
    
    try:
        await AccountModel.filter(pk=id).update(**account_request.dict())
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f'{e}')

    account = await AccountModel.filter(pk=id, user_id=current_user.id).first().prefetch_related('type_account')

    return account


@account_router.get(
    '/{id}',
    name='Get By Account.',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=AccountResponse
)
async def get_create(
    id: UUID,
    current_user: UserModel = Depends(get_current_user)
):
    account = await AccountModel.filter(pk=id, user_id=current_user.id).first().prefetch_related('type_account')
    if account is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Account information does not match {id}.')
    
    return account

# @account_router.patch(
#     '/{id}',
#     name='Change amount Account.',
#     status_code=status.HTTP_202_ACCEPTED,
#     response_model=AccountResponse
# )
# async def change_amount_account(id: UUID, amount: AmountRequest, current_user: UserModel = Depends(get_current_user)):
#     pass


@account_router.delete(
    '/{id}',
    name='Delete Account.',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_create(
    id: UUID,
    current_user: UserModel = Depends(get_current_user)
):
    amount = await AccountModel.filter(pk=id, user_id=current_user.id).first()
    if amount is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Account information does not match {id}.')
    
    if amount.amount > 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='The account has money, it cannot be deleted without withdrawing all the money.')
    
    await amount.delete()
    return