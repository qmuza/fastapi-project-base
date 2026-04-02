from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import CurrentUser, UserResponse
from app.services import get_user_by_username
from app.utils.token import verify_token


async def get_current_user(
    payload: dict = Depends(verify_token),
    db: AsyncSession = Depends(get_db)
) -> CurrentUser:
    user_type = payload.get("user_type")
    user_identifier = payload.get("user")
    
    if user_type in ["basic"]:
        db_user = await get_user_by_username(db, user_identifier)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return CurrentUser(
            user_type=user_type,
            user=UserResponse.model_validate(db_user)
        )
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid user type"
    )
