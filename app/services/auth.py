from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import User
from app.schemas import LoginForm
from app.utils import verify_password

async def verify_user(db: AsyncSession, form: LoginForm) -> bool:
    result = db.execute(select(User).where(User.username == form.username))
    user = result.scalar_one_or_none()
    if user:
        return verify_password(form.username, user.hashed_password)

    return False