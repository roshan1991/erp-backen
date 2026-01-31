from fastapi.testclient import TestClient
from app.main import app
from app.api.v1.login import router

client = TestClient(app)

def test_login():
    login_data = {
        "username": "admin",
        "password": "admin"
    }
    response = client.post("/api/v1/login/access-token", data=login_data)
    with open("login_test_result.txt", "w") as f:
        if response.status_code == 200:
            print("Login Successful!")
            f.write(f"Login Successful! {response.json()}")
        else:
            print(f"Login Failed: {response.status_code}")
            f.write(f"Login Failed: {response.status_code} {response.json()}")

if __name__ == "__main__":
    try:
        test_login()
    except Exception as e:
        with open("login_test_result.txt", "w") as f:
            f.write(f"Script Error: {e}")
