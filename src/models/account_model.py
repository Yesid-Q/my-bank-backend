from tortoise.fields import BigIntField, CharField, FloatField, UUIDField
from tortoise.fields.relational import ForeignKeyField

from src.models.base_model import BaseModel

class AccountModel(BaseModel):
    id = UUIDField(pk=True)
    alias = CharField(max_length=40)
    bank = CharField(max_length=100)
    number_account = CharField(max_length=11, unique=True)
    amount = FloatField(default=0)
    user = ForeignKeyField('models.UserModel', related_name='user_accounts')
    type_account = ForeignKeyField('models.TypeAccountModel', related_name='type_account')

    class Meta:
        table = 'accounts'
        ordering = ['created_at']
