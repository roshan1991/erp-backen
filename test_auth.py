from app.core.security import verify_password
from app.crud import crud_user
from app.db.session import SessionLocal

db = SessionLocal()
user = crud_user.get_by_username(db, username="admin")

if user:
    print(f"User found: {user.username}")
    print(f"Email: {user.email}")
    print(f"Is superuser: {user.is_superuser}")
    print(f"Is active: {user.is_active}")
    
    # Test password
    password_correct = verify_password("admin", user.hashed_password)
    print(f"\nPassword 'admin' is correct: {password_correct}")
    
    # Test authentication function
    auth_user = crud_user.authenticate(db, username="admin", password="admin")
    print(f"Authentication successful: {auth_user is not None}")
else:
    print("User not found!")

db.close()
