import sys
try:
    import psycopg2
    print("WARNING: psycopg2 IS installed.")
except ImportError:
    print("SUCCESS: psycopg2 is NOT installed.")

from app.core.config import settings
print(f"DB URI: {settings.SQLALCHEMY_DATABASE_URI}")

if "postgresql" in settings.SQLALCHEMY_DATABASE_URI:
    print("FAIL: URI still contains postgresql")
elif "mysql" in settings.SQLALCHEMY_DATABASE_URI:
    print("SUCCESS: URI contains mysql")
else:
    print("UNKNOWN URI format")
