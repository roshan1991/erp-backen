from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.crud import crud_user
from app.schemas.user import UserCreate

def init_db(db: Session) -> None:
    user = crud_user.get_by_username(db, username="admin")
    if not user:
        user_in = UserCreate(
            username="admin",
            email="admin@example.com",
            password="admin",
            is_superuser=True,
            full_name="Initial Admin",
        )
        user = crud_user.create(db, obj_in=user_in)
        print("Superuser created")
    else:
        print("Superuser already exists")

if __name__ == "__main__":
    try:
        db = SessionLocal()
        init_db(db)
        with open("initial_data_status.txt", "w") as f:
            f.write("Generic Success")
    except Exception as e:
        with open("initial_data_status.txt", "w") as f:
            f.write(f"Error: {e}")
