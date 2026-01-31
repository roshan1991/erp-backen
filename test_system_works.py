from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

client = TestClient(app)

def test_system_health():
    """Verify the system is running and database is accessible via API."""
    print("Testing Root Endpoint...")
    response = client.get("/")
    assert response.status_code == 200
    print(f"Root endpoint response: {response.json()}")
    
    print("\nTesting Login...")
    login_data = {
        "username": "admin",
        "password": "admin"
    }
    response = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        print("Login Successful!")
        print(f"Token acquired (truncated): {token[:20]}...")
    else:
        print(f"Login Failed: {response.status_code}")
        print(response.json())
        raise Exception("System Login Test Failed")

if __name__ == "__main__":
    try:
        test_system_health()
        print("\nSUCCESS: System is working correctly with MySQL.")
    except Exception as e:
        print(f"\nFAILURE: {e}")
        exit(1)
