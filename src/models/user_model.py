from tortoise.fields import CharField, UUIDField
from tortoise.fields.relational import ForeignKeyField, ReverseRelation

from src.models.base_model import BaseModel


class UserModel(BaseModel):
    id = UUIDField(pk=True)
    doc_number = CharField(max_length=20, unique=True)
    name = CharField(max_length=100)
    lastname = CharField(max_length=100)
    email = CharField(max_length=100, unique=True)
    phone = CharField(max_length=20, unique=True)
    password = CharField(max_length=200)
    document = ForeignKeyField('models.DocumentModel', related_name='document_user')

    accounts: ReverseRelation['AccountModel'] 

    class Meta:
        table = 'users'
        ordering = ['created_at']
