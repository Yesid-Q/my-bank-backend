from typing import Optional

from pydantic import BaseModel, constr, EmailStr, Field, validator

from src.utils.password_util import get_password


class ProfileRequest(BaseModel):
    doc_number: Optional[constr(min_length=3, max_length=20, to_lower=True, strip_whitespace=True)] = Field(None, alias='docNumber')
    name: Optional[constr(min_length=3, max_length=100, to_lower=True, strip_whitespace=True)] = Field(None)
    lastname: Optional[constr(min_length=3, max_length=100, to_lower=True, strip_whitespace=True)] = Field(None)
    email: Optional[EmailStr]  = Field(None)
    phone: Optional[constr(min_length=2, max_length=20, strip_whitespace=True)] = Field(None)


class PasswordRequest(BaseModel):
    old_password: constr(min_length=8, max_length=24, strip_whitespace=True) = Field(..., alias='oldPassword')
    verify_password: constr(min_length=8, max_length=24, strip_whitespace=True) = Field(..., alias='verifyPassword')
    new_password: constr(min_length=8, max_length=24, strip_whitespace=True) = Field(..., alias='newPassword')

    @validator('verify_password')
    def validate_verify_password(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Not match password.')
        return v
    
    @validator('new_password')
    def validate_password(cls, v):
        return get_password(v)
