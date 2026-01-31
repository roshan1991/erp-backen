import requests
import sys

BASE_URL = "http://localhost:10000/api/v1"

def test_login_and_me():
    log = []
    log.append(f"Testing API at {BASE_URL}")
    
    # 1. Login
    login_url = f"{BASE_URL}/login/access-token"
    # Using 'admin' as username, password doesn't matter due to bypass
    payload = {'username': 'admin', 'password': 'any_password'}
    
    log.append(f"\n1. Attempting login with {payload}...")
    try:
        resp = requests.post(login_url, data=payload)
        log.append(f"Login Status: {resp.status_code}")
        if resp.status_code != 200:
            log.append(f"Login Failed: {resp.text}")
            
        else:
            data = resp.json()
            token = data.get("access_token")
            log.append(f"Got Token: {token[:20]}...")

            # 2. Get Me
            me_url = f"{BASE_URL}/users/me"
            headers = {"Authorization": f"Bearer {token}"}
            
            log.append(f"\n2. Attempting GET {me_url}...")
            try:
                resp = requests.get(me_url, headers=headers)
                log.append(f"Me Status: {resp.status_code}")
                log.append(f"Me Response: {resp.text}")
            except Exception as e:
                log.append(f"Me Exception: {e}")

    except Exception as e:
        log.append(f"Login Exception: {e}")

    with open("login_test_result.txt", "w") as f:
        f.write("\n".join(log))
    print("Done")

if __name__ == "__main__":
    test_login_and_me()
