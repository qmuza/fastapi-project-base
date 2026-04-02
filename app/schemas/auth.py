from typing import Optional
from pydantic import BaseModel
from app.schemas.user import UserResponse

class LoginForm(BaseModel):
    username: Optional[str] = None # diisi email
    password: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class CurrentUser(BaseModel):
    user_type: str
    user: UserResponse
