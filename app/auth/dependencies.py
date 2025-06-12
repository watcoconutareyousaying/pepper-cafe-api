from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from typing import Optional
from fastapi import Request

from app import models
from app.database import SessionLocal
from app.config import settings
from app.crud import user as crud_user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_expectation = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get('sub')
        if user_id is None:
            raise credentials_expectation
    except (JWTError, ValueError):
        raise credentials_expectation

    
    user = crud_user.get_user_by_id(db, user_id)
    if user is None:
        raise credentials_expectation
    return user


def get_current_user_or_none(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = int(payload.get("sub"))
        return crud_user.get_user_by_id(db, user_id)
    except Exception:
        return None


def get_token_optional(request: Request) -> Optional[str]:
    authorization: str = request.headers.get("Authorization")
    if authorization:
        return authorization.replace("Bearer ", "")
    return None