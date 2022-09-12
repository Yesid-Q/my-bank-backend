from tortoise.fields import CharField, UUIDField

from src.models.base_model import BaseModel

class TypeAccountModel(BaseModel):
    id = UUIDField(pk=True)
    name = CharField(max_length=50)

    class Meta:
        table = 'type_accounts'
        ordering = ['created_at']
