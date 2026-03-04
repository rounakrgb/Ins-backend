from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_add_user():
    response = client.post(
        "/signup",
        params = {
            "username":"TestUser",
            "password":"any@1343"
        }
    )
    
    assert response.status_code == 200
    