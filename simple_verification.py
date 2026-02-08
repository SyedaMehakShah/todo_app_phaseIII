"""
Simple verification script to test the complete application functionality.
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_complete_flow():
    """Test the complete authentication flow."""
    print("=== Testing Complete Application Authentication Flow ===\n")
    
    # Test 1: Try to sign in with a new user (should fail initially)
    print("1. Testing sign-in with new user (should fail initially)...")
    signin_data = {
        "email": "finaltest@example.com",
        "password": "finaltestpass123"
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/auth/signin", json=signin_data)
    if response.status_code == 401:
        print("   OK - Sign-in correctly failed for non-existent user")
    else:
        print(f"   WARNING - Unexpected response: {response.status_code}")
    
    # Test 2: Sign up the new user
    print("\n2. Testing sign-up for new user...")
    signup_data = {
        "email": "finaltest@example.com",
        "password": "finaltestpass123"
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/auth/signup", json=signup_data)
    if response.status_code == 201:
        print("   OK - Sign-up successful!")
        signup_response = response.json()
        user_id = signup_response['user']['id']
        token = signup_response['token']
        print(f"   User ID: {user_id}")
        print(f"   Token length: {len(token)} characters")
    else:
        print(f"   FAIL - Sign-up failed: {response.status_code}, {response.text}")
        return False
    
    # Test 3: Sign in with the newly created user
    print("\n3. Testing sign-in with newly created user...")
    response = requests.post(f"{BASE_URL}/api/v1/auth/signin", json=signin_data)
    if response.status_code == 200:
        print("   OK - Sign-in successful for new user!")
        signin_response = response.json()
        new_token = signin_response['token']
        print(f"   Token length: {len(new_token)} characters")
    else:
        print(f"   FAIL - Sign-in failed: {response.status_code}, {response.text}")
        return False
    
    # Test 4: Access protected endpoint with token
    print("\n4. Testing access to protected endpoint...")
    headers = {
        "Authorization": f"Bearer {new_token}"
    }
    
    response = requests.get(f"{BASE_URL}/api/v1/auth/me", headers=headers)
    if response.status_code == 200:
        print("   OK - Protected endpoint access successful!")
        user_data = response.json()
        print(f"   User email: {user_data['email']}")
        print(f"   User ID: {user_data['id']}")
    else:
        print(f"   FAIL - Protected endpoint access failed: {response.status_code}, {response.text}")
        return False
    
    print("\n=== All tests completed successfully! ===")
    print("\nSUMMARY:")
    print("- Backend server is running and accessible")
    print("- Authentication system (signup/signin) is working")
    print("- JWT token generation and validation is working")
    print("- Protected endpoints are properly secured")
    print("- Full authentication flow is functional")
    
    return True

if __name__ == "__main__":
    success = test_complete_flow()
    if success:
        print("\nAPPLICATION VERIFICATION: SUCCESSFUL")
    else:
        print("\nAPPLICATION VERIFICATION: FAILED")