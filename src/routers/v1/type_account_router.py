from uuid import UUID
from typing import List

from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from tortoise.exceptions import IntegrityError

from src.models.type_account_model import TypeAccountModel
from src.schemas.type_account_schema import TypeAccountRequest, TypeAccountResponse

type_account_router = APIRouter(
    prefix='/type_account',
    tags=['type account']
)


@type_account_router.get(
    '',
    name='All Types Account.',
    status_code=status.HTTP_200_OK,
    response_model=List[TypeAccountResponse]
)
async def get_all():
    type_accounts = await TypeAccountModel.filter(deleted_at__not_isnull=False)
    return type_accounts


@type_account_router.post(
    '',
    name='Create Type Account.',
    status_code=status.HTTP_201_CREATED,
    response_model=TypeAccountResponse
)
async def create_type_account(type_account_data: TypeAccountRequest):
    try:
        type_account = await TypeAccountModel.create(**type_account_data.dict())
    except IntegrityError as err:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f'{err}')
    return type_account


@type_account_router.get(
    '/{id}',
    name='Get by Id Type Account.',
    status_code=status.HTTP_200_OK,
    response_model=TypeAccountResponse
)
async def get_type_account(id: UUID):
    type_account = await TypeAccountModel.get_or_none(pk=id)
    if type_account is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Not found type account with id {id}')
    return type_account


@type_account_router.put(
    '/{id}',
    name='Update Type Account.',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=TypeAccountResponse
)
async def get_type_account(id: UUID, type_account_data: TypeAccountRequest):
    check = await TypeAccountModel.get_or_none(pk=id)
    if check is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Not found type account with id {id}')
    try:
        await TypeAccountModel.filter(pk=id).update(**type_account_data.dict())
        type_account = await TypeAccountModel.filter(pk=id).first()
    except IntegrityError as err:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f'{err}')

    return type_account


@type_account_router.delete(
    '/{id}',
    name='Delete Type Account.',
    status_code=status.HTTP_204_NO_CONTENT
)
async def get_type_account(id: UUID):
    type_account = await TypeAccountModel.get_or_none(pk=id)
    if type_account is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Not found type account with id {id}')
    await type_account.delete()
    return

