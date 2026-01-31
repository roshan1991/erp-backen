import pymysql
import sys
from app.core.config import settings

print(f"Testing MySQL connection to {settings.MYSQL_SERVER}:{settings.MYSQL_PORT} for user '{settings.MYSQL_USER}'...")

try:
    conn = pymysql.connect(
        host=settings.MYSQL_SERVER,
        port=int(settings.MYSQL_PORT),
        user=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD,
        database=settings.MYSQL_DB,
        connect_timeout=5
    )
    print("MySQL Connection SUCCESSFUL!")
    conn.close()
    sys.exit(0)
except pymysql.err.OperationalError as e:
    print(f"MySQL Connection FAILED: {e}")
    sys.exit(1)
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)
