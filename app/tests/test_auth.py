import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_success():
    response = client.post("auth/login", json={"username": "bhive_user", "password": "bhive_backend_secret_password"})
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert "expire_at" in data
    assert data["refresh_token"] == ""

def test_login_failure_invalid_credentials():
    response = client.post("auth/login", json={"username": "invaliduser", "password": "wrongpassword"})
    assert response.status_code == 401

def test_login_failure_missing_fields():
    response = client.post("auth/login", json={})  # Sending empty payload
    assert response.status_code == 422  # Unprocessable Entity for missing fields

def test_login_failure_missing_username():
    response = client.post("auth/login", json={"password": "testpassword"})
    assert response.status_code == 422  # Unprocessable Entity for missing username

def test_login_failure_missing_password():
    response = client.post("auth/login", json={"username": "testuser"})
    assert response.status_code == 422  # Unprocessable Entity for missing password
