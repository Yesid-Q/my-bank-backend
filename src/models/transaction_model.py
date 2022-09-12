from tortoise.fields import CharField, FloatField, UUIDField, SmallIntField
from tortoise.fields.relational import ForeignKeyField, ReverseRelation, ForeignKeyNullableRelation

from src.models.base_model import BaseModel


class TransactionModel(BaseModel):
    id = UUIDField(pk=True)
    amount = FloatField()
    action = SmallIntField()
    owner: ForeignKeyNullableRelation = ForeignKeyField('models.UserModel', related_name='transaction_owner', null=True)
    account_owner: ForeignKeyNullableRelation = ForeignKeyField('models.AccountModel', related_name='account_owner', null=True)
    receiver = ForeignKeyField('models.UserModel', related_name='transaction_receiver')
    account_receiver = ForeignKeyField('models.AccountModel', related_name='account_receiver')
    
    class Meta:
        table = 'transactions'
        ordering = ['created_at']
