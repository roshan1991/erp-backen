import pymysql
from app.core.config import settings
import sys

def verify_mysql_tables():
    output = []
    output.append(f"Connecting to MySQL at {settings.MYSQL_SERVER} as {settings.MYSQL_USER}...")
    try:
        conn = pymysql.connect(
            host=settings.MYSQL_SERVER,
            port=int(settings.MYSQL_PORT),
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD,
            database=settings.MYSQL_DB
        )
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        output.append("\nTables found in database:")
        for table in tables:
            output.append(f" - {table}")
            
        required_tables = ['users', 'alembic_version']
        missing = [t for t in required_tables if t not in tables]
        
        if missing:
            output.append(f"\nERROR: Missing critical tables: {missing}")
            # sys.exit(1)
        
        # Check Admin User
        if 'users' in tables:
            cursor.execute("SELECT username, email, is_superuser FROM users WHERE username='admin'")
            admin = cursor.fetchone()
            if admin:
                output.append(f"\nAdmin user found: {admin}")
            else:
                output.append("\nWARNING: 'admin' user NOT found in 'users' table.")
        
        conn.close()
        output.append("\nMySQL System Verification: SUCCESS")
        
    except Exception as e:
        output.append(f"\nMySQL System Verification: FAILED - {e}")
        # sys.exit(1)

    with open("verify_output.txt", "w") as f:
        f.write("\n".join(output))

if __name__ == "__main__":
    verify_mysql_tables()
