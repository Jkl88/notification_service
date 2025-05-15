from fastapi import APIRouter, Depends
from app.schemas.auth import RegisterRequest, TokenResponse, LoginRequest
from app.services.auth import register_user, login_user, refresh_access_token
from app.core.dependencies import refresh_scheme
from fastapi.security import HTTPAuthorizationCredentials

router = APIRouter()

@router.post("/register", response_model=TokenResponse)
async def register(data: RegisterRequest):
    return await register_user(data)
    
@router.post("/login")
async def login(data: LoginRequest = Depends()):
    return await login_user(data)
    
@router.post("/refresh")
async def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(refresh_scheme)):
    return await refresh_access_token(credentials)