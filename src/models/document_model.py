from tortoise.fields import CharField

from src.models.base_model import BaseModel

class DocumentModel(BaseModel):
    id = CharField(pk=True, unique=True, max_length=2)
    name = CharField(max_length=30, unique=True)

    class Meta:
        table = 'documents'
        ordering = ['created_at']

