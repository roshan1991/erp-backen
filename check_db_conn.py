import sys
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from app.core.config import settings

def check_connection():
    print(f"Testing connection to: {settings.SQLALCHEMY_DATABASE_URI}")
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, connect_args={"connect_timeout": 5})
    try:
        with engine.connect() as connection:
            print("Connection successful!")
    except OperationalError as e:
        print(f"Connection failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    check_connection()
