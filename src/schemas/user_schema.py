from uuid import UUID
from typing import Optional
from datetime import datetime

from pydantic import BaseModel

from src.schemas.document_schema import DocumentResponse

class UserInfo(BaseModel):
    id: UUID
    name: str
    lastname: str
    email: str
    phone: str
    

class UserResponse(BaseModel):
    id: UUID
    doc_number: str
    name: str
    lastname: str
    email: str
    phone: str
    document: DocumentResponse
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        fields = {
            'doc_number': 'docNumber',
            'created_at': 'createdAt',
            'updated_at': 'updatedAt',
            'deleted_at': 'deletedAt'
        }