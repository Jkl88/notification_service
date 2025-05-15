from app.models.user import User
from app.schemas.auth import RegisterRequest, LoginRequest
from app.core.security import hash_password, create_access_token, create_refresh_token, verify_password
from app.config import settings
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from app.core.logger import logger


async def register_user(data: RegisterRequest):
    logger.info(f"Регистрация нового пользователя: {data.username}")
    user = await User.create(
        username=data.username,
        password=hash_password(data.password)
    )
    access_token = create_access_token({"sub": str(user.id)}, settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_refresh_token({"sub": str(user.id)}, settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    return {
        "user_id": user.id,
        "access_token": access_token,
        "refresh_token": refresh_token
    }

async def login_user(data: LoginRequest):
    logger.info(f"Попытка входа: {data.username}")
    user = await User.get_or_none(username=data.username)
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": str(user.id)}, settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_access_token({"sub": str(user.id)}, settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user_id": user.id
    }

async def refresh_access_token(credentials: HTTPAuthorizationCredentials):
    refresh_token = credentials.credentials
    try:
        payload = jwt.decode(refresh_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        if payload.get("token_type") != "refresh":
            type_token = payload.get("token_type")
            raise JWTError(f"Not a refresh token (type={type_token})")
        user_id = payload.get("sub")
        if not user_id:
            raise JWTError("Missing subject")
        new_access_token = create_access_token({"sub": user_id}, settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid refresh token ({e})")
        