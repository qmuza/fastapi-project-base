from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_token(data: dict, expires_delta: timedelta = timedelta(hours=24)):
    to_encode = data.copy()
    issue_time = datetime.now(timezone.utc)
    to_encode.update({"iat": issue_time, "exp": issue_time + expires_delta})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET.encode("utf-8"), algorithm="HS256")
    return {
        "access_token": encoded_jwt,
        "token_type": "bearer",
    }

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET.encode("utf-8"), algorithms=["HS256"])
        user = payload.get("user")
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token invalid or expired"
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token invalid or expired"
        )