from fastapi import HTTPException, status
from app.models.notification import Notification
from app.schemas.notification import NotificationCreate, NotificationWithUser
from typing import List
from app.core.logger import logger
from app.core.redis import redis_client
from app.config import settings
import json


async def create_notification(user_id: int, data: NotificationCreate):
    logger.info(f"Создание уведомления: user_id={user_id}, type={data.type}")
    notification = await Notification.create(
        user_id=user_id,
        type=data.type,
        text=data.text
    )
    async for key in redis_client.scan_iter(f"notifications:{user_id}:*"):
        await redis_client.delete(key)
    return notification


async def get_notifications(user_id: int, limit: int = 10, offset: int = 0):
    cache_key = f"notifications:{user_id}:{limit}:{offset}"
    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    notifications = await Notification.filter(user_id=user_id)\
        .order_by("-created_at").offset(offset).limit(limit).prefetch_related("user")

    result = [
        NotificationWithUser(
            id=n.id,
            user_id=n.user_id,
            type=n.type,
            text=n.text,
            created_at=n.created_at,
            username=n.user.username,
            avatar_url=n.user.avatar_url,
        )
        for n in notifications
    ]

    await redis_client.set(cache_key, json.dumps([r.model_dump(mode="json") for r in result]), ex=settings.CACHE_TTL_SECONDS)
    return result
    
async def delete_notification(user_id: int, notification_id: int):
    logger.info(f"Запрос на удаление уведомления {notification_id} от пользователя {user_id}")
    notification = await Notification.get_or_none(id=notification_id)
    if not notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    if notification.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your notification")
    await notification.delete()
    async for key in redis_client.scan_iter(f"notifications:{user_id}:*"):
        await redis_client.delete(key)
    return {"detail": "Notification deleted"}
