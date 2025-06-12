from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from typing import Optional

from app.config import settings
from app.schemas.user import UserCreate, UserOut
from app.models.user import User
from app.crud import user as crud_user
from app.auth.dependencies import get_db, get_token_optional
from app.core.utils import generate_password
from app.core.constants import ROLES
from app.services.auth_service import send_password_mail


router = APIRouter(prefix="/users", tags=['users'])


@router.post('/create', response_model=UserOut)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    token: Optional[str] = Depends(get_token_optional),
    # current_user: User = Depends(get_current_user_or_none)
):
    owner_count = crud_user.get_owner_count(db)

    # First time setup: no owners exist yet
    if owner_count == 0:
        if user_in.role != "owner":
            raise HTTPException(
                status_code=403, detail="First user must be an owner.")

        generated_password = generate_password()
        user = crud_user.create_user(
            db=db, user=user_in, raw_password=generated_password)
        send_password_mail(email=user.email, password=generated_password)
        return user

    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        current_user = crud_user.get_user_by_id(db, int(user_id))
        if current_user is None or current_user.role != "owner":
            raise HTTPException(
                status_code=403, detail="Only owners can create users")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    generated_password = generate_password()
    user = crud_user.create_user(
        db=db, user=user_in, raw_password=generated_password)
    send_password_mail(email=user.email, password=generated_password)
    return user
