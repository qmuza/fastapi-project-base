from fastapi import APIRouter, Form, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.config import settings
from app.schemas import LoginForm
from app.services import auth as auth_services
from app.utils import create_token

router = APIRouter()

@router.post("/login")
async def login(form_data: LoginForm = Form(), db: AsyncSession = Depends(get_db)):
    if form_data.username and form_data.password:        
        matching_creds = await auth_services.verify_user(form_data)
        if matching_creds:
            return create_token({
                "user": form_data.username,
                "user_type": "basic"
            })
        
        raise HTTPException(status_code=401, detail="Incorrect Username or Password")

    raise HTTPException(status_code=400, detail="Missing Credentials")


