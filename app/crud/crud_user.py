from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

def get_by_email(db: Session, *, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def get_by_username(db: Session, *, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def get(db: Session, *, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_multi(db: Session, *, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()

def create(db: Session, *, obj_in: UserCreate) -> User:
    db_obj = User(
        username=obj_in.username,
        email=obj_in.email,
        hashed_password=get_password_hash(obj_in.password),
        full_name=obj_in.full_name,
        is_superuser=obj_in.is_superuser,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]) -> User:
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.model_dump(exclude_unset=True)
    
    if "password" in update_data:
        hashed_password = get_password_hash(update_data["password"])
        del update_data["password"]
        update_data["hashed_password"] = hashed_password
    
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete(db: Session, *, user_id: int) -> Optional[User]:
    user = get(db, user_id=user_id)
    if user:
        db.delete(user)
        db.commit()
    return user

def authenticate(db: Session, *, username: str, password: str) -> Optional[User]:
    user = get_by_username(db, username=username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
