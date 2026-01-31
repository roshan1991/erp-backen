import pymysql
from app.core.config import settings

log = []
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
    log.append(f"Tables: {tables}")
    
    if 'user' in tables and 'users' not in tables:
        log.append("Renaming 'user' to 'users'...")
        cursor.execute("RENAME TABLE user TO users")
        log.append("Success.")
    elif 'users' in tables:
        log.append("'users' table already exists.")
    else:
        log.append("'user' table not found, and 'users' not found.")
        
    conn.commit()
    conn.close()
except Exception as e:
    log.append(f"Error: {e}")

with open("rename_log.txt", "w") as f:
    f.write("\n".join(log))
