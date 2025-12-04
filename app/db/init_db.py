import logging
from sqlalchemy.orm import Session

from app.crud import crud_user
from app.schemas.user import UserCreate
from app.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db(db: Session) -> None:
    # Create super admin user if it doesn't exist
    user = crud_user.get_by_username(db, username="admin")
    if not user:
        user_in = UserCreate(
            username="admin",
            email="admin@erp.com",
            password="admin",
            full_name="Super Admin",
            is_superuser=True,
        )
        user = crud_user.create(db, obj_in=user_in)
        logger.info("Super admin user created")
    else:
        logger.info("Super admin user already exists")

def main() -> None:
    logger.info("Creating initial data")
    db = SessionLocal()
    init_db(db)
    logger.info("Initial data created")

if __name__ == "__main__":
    main()
