"""
Test script to verify sign-in and sign-up functionality.
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_signup():
    """Test the signup endpoint."""
    print("Testing signup...")
    
    signup_data = {
        "email": "testuser123@example.com",
        "password": "testpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/auth/signup", json=signup_data)
    print(f"Signup response status: {response.status_code}")
    
    if response.status_code == 201:
        print("Signup successful!")
        response_data = response.json()
        print(f"Token received: {response_data.get('token', '')[:20]}...")
        return response_data.get('token')
    else:
        print(f"Signup failed: {response.text}")
        return None

def test_signin():
    """Test the signin endpoint."""
    print("\nTesting signin...")
    
    signin_data = {
        "email": "testuser123@example.com",
        "password": "testpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/auth/signin", json=signin_data)
    print(f"Signin response status: {response.status_code}")
    
    if response.status_code == 200:
        print("Signin successful!")
        response_data = response.json()
        print(f"Token received: {response_data.get('token', '')[:20]}...")
        return response_data.get('token')
    else:
        print(f"Signin failed: {response.text}")
        return None

def test_protected_endpoint(token):
    """Test accessing a protected endpoint with the token."""
    if not token:
        print("\nCannot test protected endpoint without token.")
        return
    
    print("\nTesting protected endpoint (get user profile)...")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(f"{BASE_URL}/api/v1/auth/me", headers=headers)
    print(f"Protected endpoint response status: {response.status_code}")
    
    if response.status_code == 200:
        print("Protected endpoint access successful!")
        response_data = response.json()
        print(f"User data: {json.dumps(response_data, indent=2)}")
    else:
        print(f"Protected endpoint access failed: {response.text}")

if __name__ == "__main__":
    print("Starting authentication functionality test...\n")
    
    # Test signup
    signup_token = test_signup()
    
    # Test signin
    signin_token = test_signin()
    
    # Test protected endpoint with signin token
    test_protected_endpoint(signin_token)
    
    print("\nAuthentication test completed!")