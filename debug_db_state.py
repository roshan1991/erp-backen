import pymysql
import sys
from app.core.config import settings

print(f"Connecting to {settings.MYSQL_SERVER}...")
try:
    conn = pymysql.connect(
        host=settings.MYSQL_SERVER,
        port=int(settings.MYSQL_PORT),
        user=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD,
        database=settings.MYSQL_DB
    )
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = [t[0] for t in cursor.fetchall()]
    print("Tables in DB:", tables)
    
    if 'users' in tables:
        print("Table 'users' matches normal convention.")
        cursor.execute("SELECT count(*) FROM users")
        print(f"Rows in 'users': {cursor.fetchone()[0]}")
        cursor.execute("SELECT id, username FROM users LIMIT 1")
        print(f"Sample user: {cursor.fetchone()}")
        
    if 'user' in tables:
        print("Table 'user' exists (legacy?).")
        cursor.execute("SELECT count(*) FROM user")
        print(f"Rows in 'user': {cursor.fetchone()[0]}")

    conn.close()

except Exception as e:
    print(f"Error: {e}")
