import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from app.core.config import settings

def create_database():
    try:
        # Connect to default postgres database
        con = psycopg2.connect(
            dbname="postgres",
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_SERVER,
            port=settings.POSTGRES_PORT
        )
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        
        # Check if database exists
        cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{settings.POSTGRES_DB}'")
        exists = cur.fetchone()
        
        if not exists:
            print(f"Creating database {settings.POSTGRES_DB}...")
            cur.execute(f"CREATE DATABASE {settings.POSTGRES_DB}")
            print("Database created successfully.")
        else:
            print(f"Database {settings.POSTGRES_DB} already exists.")
            
        cur.close()
        con.close()
    except Exception as e:
        print(f"Error creating database: {e}")

if __name__ == "__main__":
    create_database()
