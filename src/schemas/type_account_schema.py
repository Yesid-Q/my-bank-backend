from uuid import UUID
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, constr, Field


class TypeAccountRequest(BaseModel):
    name: constr(min_length=2, max_length=50, to_lower=True, strip_whitespace=True) = Field(...)

class TypeAccountResponse(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        fields = {
            'created_at': 'createdAt',
            'updated_at': 'updatedAt',
            'deleted_at': 'deletedAt'
        }
