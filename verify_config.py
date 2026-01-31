from app.core.config import settings

print(f"DB_TYPE: {settings.DB_TYPE}")
print(f"URI: {settings.SQLALCHEMY_DATABASE_URI}")
