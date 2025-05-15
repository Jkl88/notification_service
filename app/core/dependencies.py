from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from app.config import settings

access_scheme = HTTPBearer(
    scheme_name="Access token"
)

refresh_scheme = HTTPBearer(
    scheme_name="Refresh token"
)

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(access_scheme)) -> int:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        if payload.get("token_type") != "access":
            raise JWTError(f"Not an access token(type={type_token})")
        user_id = payload.get("sub")
        if user_id is None:
            raise JWTError("Missing subject")
        return int(user_id)
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid access token ({e})")