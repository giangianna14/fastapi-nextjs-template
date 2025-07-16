from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_protected_route_unauthorized():
    response = client.get("/api/v1/user/protected")
    assert response.status_code == 401

def test_protected_route_authorized():
    # Login dulu untuk dapatkan token
    login = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"}
    )
    assert login.status_code == 200
    token = login.json()["access_token"]

    # Akses endpoint dengan token
    response = client.get(
        "/api/v1/user/protected",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "user"
