from typing import List
from fastapi import APIRouter, Depends, Query, HTTPException, status
from app.schemas.notification import NotificationCreate, NotificationOut, NotificationWithUser
from app.services.notifications import create_notification, get_notifications, delete_notification
from app.core.dependencies import get_current_user_id

router = APIRouter()

@router.post("/", response_model=NotificationOut)
async def create(data: NotificationCreate, user_id: int = Depends(get_current_user_id)):
    return await create_notification(user_id, data)

@router.get("/", response_model=List[NotificationWithUser])
async def read(limit: int = Query(10, ge=1), offset: int = Query(0, ge=0), user_id: int = Depends(get_current_user_id)):
    return await get_notifications(user_id=user_id, limit=limit, offset=offset)
    
@router.delete("/{notification_id}")
async def delete(notification_id: int, user_id: int = Depends(get_current_user_id)):
    return await delete_notification(user_id=user_id, notification_id=notification_id)