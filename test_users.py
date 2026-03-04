from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_add_user():
    response = client.post(
    "/signup",
    json={
        "username": "TestUser",
        "password": "any@1343"
    }
    )
    
    assert response.status_code == 200
    