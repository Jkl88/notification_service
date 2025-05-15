from pydantic import BaseModel


class RegisterRequest(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    user_id: int
    access_token: str
    refresh_token: str