# test_api.py

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_user_signup():
    """Test user signup"""
    url = f"{BASE_URL}/users/signup"
    data = {
        "name": "Test Parent",
        "email": "test@example.com",
        "password": "SecurePass123"
    }
    
    print("Testing user signup...")
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    return response

def test_user_login():
    """Test user login"""
    url = f"{BASE_URL}/users/login"
    data = {
        "email": "test@example.com",
        "password": "SecurePass123"
    }
    
    print("\nTesting user login...")
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        return response.json().get("access_token")
    return None

def test_kid_signup(token):
    """Test kid signup"""
    url = f"{BASE_URL}/kids/signup"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "name": "Zaid",
        "age_group": "5-8",
        "gender": "M"
    }
    
    print(f"\nTesting kid signup...")
    print(f"Data: {data}")
    response = requests.post(url, json=data, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    return response

if __name__ == "__main__":
    # Test user signup
    test_user_signup()
    
    # Test user login
    token = test_user_login()
    
    if token:
        # Test kid signup
        test_kid_signup(token)
    else:
        print("Failed to get token, skipping kid signup test") 