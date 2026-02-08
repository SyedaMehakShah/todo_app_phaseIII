"""
Debug script to test the FastAPI app directly
"""
from src.main import app
import uvicorn
from fastapi.testclient import TestClient

# Test with TestClient to see if routes work
print("Testing routes with TestClient...")
client = TestClient(app)

# Test the health endpoint first
response = client.get("/")
print(f"Root endpoint: {response.status_code}, {response.json()}")

# Test auth endpoint
response = client.post("/api/v1/auth/signup", 
                      json={"email": "debug@example.com", "password": "testpassword123"})
print(f"Signup endpoint: {response.status_code}, {response.json()}")

# Test tasks endpoint
response = client.post("/api/v1/tasks", 
                      json={"title": "Debug task", "description": "Debug task"},
                      headers={"Authorization": "Bearer dummy_token"})
print(f"Tasks endpoint: {response.status_code}, {response.text}")

print("\nStarting server with uvicorn...")
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)