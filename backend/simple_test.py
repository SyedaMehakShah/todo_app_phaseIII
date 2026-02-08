"""
Simple test to check if the routes are working properly
"""
from requests import Session
from starlette.testclient import TestClient
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

from src.main import app

def test_routes():
    print("Testing routes directly with TestClient...")
    client = TestClient(app)
    
    # Test the root endpoint
    response = client.get("/")
    print(f"Root endpoint: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test the health endpoint
    response = client.get("/health")
    print(f"Health endpoint: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test the tasks endpoint (should return 401 since no auth)
    response = client.get("/api/v1/tasks")
    print(f"Tasks GET endpoint: {response.status_code}")
    print(f"Response: {response.text}")
    
    # Test the tasks endpoint with a dummy auth header
    response = client.post("/api/v1/tasks", 
                          json={"title": "Test", "description": "Test"},
                          headers={"Authorization": "Bearer dummy"})
    print(f"Tasks POST endpoint: {response.status_code}")
    print(f"Response: {response.text}")
    
    # Print all routes for reference
    print("\nAll registered routes:")
    for route in app.routes:
        if hasattr(route, 'methods') and hasattr(route, 'path'):
            print(f"  {route.methods} {route.path}")

if __name__ == "__main__":
    test_routes()