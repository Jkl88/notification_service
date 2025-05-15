from tortoise import fields
from tortoise.models import Model
from enum import Enum

from app.models.user import User


class NotificationType(str, Enum):
    like = "like"
    comment = "comment"
    repost = "repost"


class Notification(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="notifications")
    type = fields.CharEnumField(enum_type=NotificationType, max_length=10)
    text = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
