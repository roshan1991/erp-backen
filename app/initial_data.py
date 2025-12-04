from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.crud import crud_user
from app.schemas.user import UserCreate

def init_db(db: Session) -> None:
    user = crud_user.get_by_email(db, email="admin@example.com")
    if not user:
        user_in = UserCreate(
            email="admin@example.com",
            password="password",
            is_superuser=True,
            full_name="Initial Admin",
        )
        user = crud_user.create(db, obj_in=user_in)
        print("Superuser created")
    else:
        print("Superuser already exists")

if __name__ == "__main__":
    db = SessionLocal()
    init_db(db)
