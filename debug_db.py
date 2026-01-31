import sys
import os
from sqlalchemy import create_engine, text
from app.core.config import settings

def test_connection():
    uri = settings.SQLALCHEMY_DATABASE_URI
    print(f"--- Database Debug Info ---")
    print(f"DB_TYPE: {settings.DB_TYPE}")
    print(f"URI: {uri}")
    print(f"Server: {settings.POSTGRES_SERVER}, Port: {settings.POSTGRES_PORT}")
    
    try:
        engine = create_engine(uri)
        # Try to connect
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print(f"Connection Successful! Result: {result.scalar()}")
    except Exception as e:
        print(f"Connection FAILED.")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Message: {e}")
        # Print detailed traceback if possible
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_connection()
