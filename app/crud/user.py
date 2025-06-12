from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.auth.security import get_password_hash


def create_user(db: Session, user: UserCreate, raw_password: str):
    hashed_password = get_password_hash(raw_password)
    db_user = User(
        name=user.name,
        email=user.email,
        role=user.role,
        hashed_password=hashed_password,    
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_owner_count(db: Session):
    return db.query(User).filter(User.role == "owner").count()