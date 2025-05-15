from tortoise import fields
from tortoise.models import Model

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=255)
    avatar_url = fields.CharField(max_length=255, default="default.avatar.jpg")
    created_at = fields.DatetimeField(auto_now_add=True)

    notifications: fields.ReverseRelation["Notification"]
