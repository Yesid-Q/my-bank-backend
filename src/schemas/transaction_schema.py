from uuid import UUID

from pydantic import BaseModel, constr, Field, conint

from src.schemas.user_schema import UserInfo
from src.schemas.account_schema import AccountInfo


class TransactionForm(BaseModel):
    number_account: constr(max_length=11, strip_whitespace=True) = Field(..., alias='numberAccount')
    password: constr(min_length=8, max_length=24, strip_whitespace=True) = Field(...)
    amount: conint(ge=0) = Field(...)


class TransactionResponse(BaseModel):
    id: UUID
    amount: float
    action: int
    owner: UserInfo
    account_owner: AccountInfo
    receiver: UserInfo
    account_receiver: AccountInfo

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        fields = {
            'account_owner': 'accountOwner',
            'account_receiver': 'accountReceiver'
        }