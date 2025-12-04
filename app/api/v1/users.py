from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import crud_user
from app.models.user import User
from app.schemas.user import User as UserSchema, UserCreate, UserUpdate

router = APIRouter()

@router.get("/users", response_model=List[UserSchema])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users. Super admin only.
    """
    users = crud_user.get_multi(db, skip=skip, limit=limit)
    return users

@router.post("/users", response_model=UserSchema)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user. Super admin only.
    """
    user = crud_user.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with this username already exists.",
        )
    user = crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with this email already exists.",
        )
    user = crud_user.create(db, obj_in=user_in)
    return user

@router.get("/users/me", response_model=UserSchema)
def read_user_me(
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user

@router.get("/users/{user_id}", response_model=UserSchema)
def read_user_by_id(
    user_id: int,
    current_user: User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id. Super admin only.
    """
    user = crud_user.get(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    return user

@router.put("/users/{user_id}", response_model=UserSchema)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: UserUpdate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a user. Super admin only.
    """
    user = crud_user.get(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    user = crud_user.update(db, db_obj=user, obj_in=user_in)
    return user

@router.delete("/users/{user_id}", response_model=UserSchema)
def delete_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete a user. Super admin only.
    """
    user = crud_user.get(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    if user.id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Users cannot delete themselves",
        )
    user = crud_user.delete(db, user_id=user_id)
    return user
