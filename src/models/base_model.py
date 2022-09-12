from datetime import datetime

from tortoise import Model
from tortoise.fields import DatetimeField, UUIDField

class BaseModel(Model):
    created_at = DatetimeField(auto_now_add=True)
    updated_at = DatetimeField(auto_now=True)
    deleted_at = DatetimeField(null=True)

    class Meta:
        abstract = True
        ordering = ['created_at']


    async def delete(self)-> None:
        self.delete_at = datetime.now() if self.delete_at is None else None
        await self.save()
