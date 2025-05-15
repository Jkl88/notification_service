from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class NotificationType(str, Enum):
    like = "like"
    comment = "comment"
    repost = "repost"


class NotificationCreate(BaseModel):
    type: NotificationType
    text: str


class NotificationOut(BaseModel):
    id: int
    user_id: int
    type: NotificationType
    text: str
    created_at: datetime

    class Config:
        from_attributes = True
        
class NotificationWithUser(BaseModel):
    id: int
    user_id: int
    type: NotificationType
    text: str
    created_at: datetime
    username: str
    avatar_url: str

    class Config:
        from_attributes = True
