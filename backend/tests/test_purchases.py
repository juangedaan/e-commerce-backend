from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_purchase():
    # Assumes user ID 1 and product ID 1 exist
    response = client.post("/purchases/", json={
        "user_id": 1,
        "product_id": 1,
        "quantity": 2
    })
    assert response.status_code == 200
    assert response.json()["quantity"] == 2

def test_get_user_purchases():
    response = client.get("/purchases/user/1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

