from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: int, token_type: str = "access"):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({
        "exp": expire,
        "token_type": token_type,
    })
    return jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

def create_refresh_token(data: dict, expires_delta: int):
    return create_access_token(data, expires_delta, token_type="refresh")