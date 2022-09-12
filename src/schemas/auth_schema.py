from uuid import UUID

from pydantic import BaseModel, Field, constr, EmailStr, validator


class LoginSchema(BaseModel):
    username: constr(min_length=2, max_length=20, strip_whitespace=True) = Field(..., alias='phone')
    password: str


class RegisterRequest(BaseModel):
    doc_number: constr(min_length=3, max_length=20, to_lower=True, strip_whitespace=True) = Field(..., alias='docNumber')
    name: constr(min_length=3, max_length=100, to_lower=True, strip_whitespace=True) = Field(...)
    lastname: constr(min_length=3, max_length=100, to_lower=True, strip_whitespace=True) = Field(...)
    email: EmailStr  = Field(...)
    phone: constr(min_length=2, max_length=20, strip_whitespace=True) = Field(...)
    password: constr(min_length=8, max_length=24, strip_whitespace=True) = Field(...)
    verify_password: constr(min_length=8, max_length=24, strip_whitespace=True) = Field(..., alias='verifyPassword')
    document_id: constr(min_length=2, max_length=2, to_lower=True, strip_whitespace=True) = Field(..., alias='documentId')

    @validator('doc_number')
    def validate_doc_number(cls, v: str):
        if not v.isnumeric():
            raise ValueError('Number document no validate.')
        return v

    @validator('email')
    def to_lower_email(cls, v):
        return v.lower()

    @validator('verify_password')
    def validate_verify_password(cls, v, values):
        print(values, v)
        if 'password' in values and v != values['password']:
            raise ValueError('Not match password.')
        return v

