from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/users/", json={"username": "alice", "email": "alice@example.com"})
    assert response.status_code == 200
    assert response.json()["username"] == "alice"

def test_get_user():
    # First, create the user
    client.post("/users/", json={"username": "bob", "email": "bob@example.com"})
    # Then, get it
    response = client.get("/users/2")  # assumes second user
    assert response.status_code == 200
    assert response.json()["email"] == "bob@example.com"

