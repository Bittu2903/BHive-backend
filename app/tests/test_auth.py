import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.helpers.database import SessionLocal, Base, engine
from app.modules.auth.models import User
from passlib.context import CryptContext

client = TestClient(app)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    test_user = User(username="bhive_user", password=pwd_context.hash("bhive_backend_secret_password"))
    db.add(test_user)
    db.commit()
    db.close()

    yield 

    Base.metadata.drop_all(bind=engine)

def test_login_success():
    response = client.post("/auth/login", json={"username": "bhive_user", "password": "bhive_backend_secret_password"})
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert "expire_at" in data
    assert data["refresh_token"] == ""

def test_login_failure_invalid_credentials():
    response = client.post("/auth/login", json={"username": "invaliduser", "password": "wrongpassword"})
    assert response.status_code == 401

def test_login_failure_missing_fields():
    response = client.post("/auth/login", json={})
    assert response.status_code == 422

def test_login_failure_missing_username():
    response = client.post("/auth/login", json={"password": "testpassword"})
    assert response.status_code == 422 

def test_login_failure_missing_password():
    response = client.post("/auth/login", json={"username": "testuser"})
    assert response.status_code == 422

def test_signup_success():
    response = client.post("/auth/signup", json={"username": "newuser", "password": "newpassword"})
    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully."}

def test_signup_failure_duplicate_user():
    response = client.post("/auth/signup", json={"username": "bhive_user", "password": "anotherpassword"})
    assert response.status_code == 400
    assert response.json() == {"detail": "User already exists."}

def test_signup_failure_missing_fields():
    response = client.post("/auth/signup", json={})
    assert response.status_code == 422

def test_signup_failure_missing_username():
    response = client.post("/auth/signup", json={"password": "testpassword"})
    assert response.status_code == 422

def test_signup_failure_missing_password():
    response = client.post("/auth/signup", json={"username": "testuser"})
    assert response.status_code == 422 
