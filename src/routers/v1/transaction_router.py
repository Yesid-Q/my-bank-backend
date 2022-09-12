from uuid import UUID
from typing import List

from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException

from tortoise.queryset import Q

from src.utils.token_util import get_current_user
from src.models.user_model import UserModel
from src.models.transaction_model import TransactionModel
from src.models.account_model import AccountModel
from src.schemas.transaction_schema import TransactionForm, TransactionResponse
from src.utils.password_util import verify_password


transaction_router = APIRouter(
    prefix='/transaction',
    tags=['transaction']
)

@transaction_router.get(
    '',
    name='Get all my transactions.',
    status_code=status.HTTP_200_OK,
    response_model=List[TransactionResponse]
)
async def get_all_my_transaction(current_user: UserModel = Depends(get_current_user)):
    transactions = await TransactionModel.filter(Q(Q(owner_id=current_user.id), Q(receiver_id=current_user.id), join_type='OR')).prefetch_related('owner', 'account_owner', 'receiver', 'account_receiver')
    return transactions


@transaction_router.put(
    '/{id}'
)
async def send_transactions(
    id: UUID,
    request: TransactionForm,
    current_user: UserModel = Depends(get_current_user)
):
    print(id, request, current_user)
    if not verify_password(request.password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can not do this operation."
        )

    account_receiver = await AccountModel.filter(number_account=request.number_account).first()

    if account_receiver is None:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="cuenta no existente."
        )

    account_owner = await AccountModel.filter(pk=id).first()

    if account_owner.amount < request.amount:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Amount insuficiente."
        )
    
    account_owner.amount -= request.amount


    account_receiver.amount += request.amount

    transaction = await TransactionModel.create(
        amount=request.amount,
        action=1,
        owner_id=current_user.id,
        account_owner_id=account_owner.id,
        receiver_id=account_receiver.user_id,
        account_receiver_id=account_receiver.id
    )

    await account_owner.save()
    await account_receiver.save()

    return transaction
