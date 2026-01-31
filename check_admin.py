from app.db.session import SessionLocal
from app.models.user import User

db = SessionLocal()
try:
    user = db.query(User).filter(User.username == "admin").first()
    if user:
        print(f"User admin exists: {user.email}")
    else:
        print("User admin does NOT exist")
except Exception as e:
    print(f"Error querying user: {e}")
finally:
    db.close()
