from uuid import UUID
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, constr, conint, Field, validator

from src.schemas.type_account_schema import TypeAccountResponse



class AccountRequest(BaseModel):
    alias: constr(strip_whitespace=True, to_lower=True, min_length=3, max_length=40) = Field(...)
    bank: constr(strip_whitespace=True, to_lower=True, min_length=3, max_length=100) = Field(...)
    amount: conint(ge=0) = Field(...)
    number_account: constr(strip_whitespace=True, to_lower=True, min_length=3, max_length=11) = Field(..., alias= 'numberAccount')
    type_account_id: UUID = Field(..., alias='typeAccountId')

    @validator('number_account')
    def validate_number_account(cls, v: str):
        if not v.isnumeric():
            raise ValueError('Number account no validate.')
        return v


class AmountRequest(BaseModel):
    amount: conint(gt=0) = Field(...)


class AccountInfo(BaseModel):
    alias: str
    bank: str
    number_account: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        fields = {
            'number_account': 'numberAccount'
        }


class AccountResponse(BaseModel):
    id: UUID
    alias: str
    bank: str
    number_account: int
    amount: float
    type_account: TypeAccountResponse
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        fields = {
            'number_account': 'numberAccount',
            'type_account': 'typeAccount',
            'created_at': 'createdAt',
            'updated_at': 'updatedAt',
            'deleted_at': 'deletedAt'
        }
