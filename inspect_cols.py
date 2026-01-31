import pymysql
from app.core.config import settings

def inspect_users_table():
    try:
        conn = pymysql.connect(
            host=settings.MYSQL_SERVER,
            port=int(settings.MYSQL_PORT),
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD,
            database=settings.MYSQL_DB
        )
        cursor = conn.cursor()
        cursor.execute("DESCRIBE users")
        columns = cursor.fetchall()
        
        with open("d:\\Projects\\erp\\backend\\user_columns.txt", "w") as f:
            f.write("Columns in users table:\n")
            for col in columns:
                f.write(f"{col}\n")
                
        print("Columns inspected.")
        conn.close()
    except Exception as e:
        with open("d:\\Projects\\erp\\backend\\user_columns.txt", "w") as f:
            f.write(f"Error: {e}")

if __name__ == "__main__":
    inspect_users_table()
