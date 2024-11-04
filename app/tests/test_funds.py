import pytest
from fastapi.testclient import TestClient
from app.helpers import env
from app.main import app
from app.helpers.database import User, get_db, Base, SessionLocal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.helpers.bcrypt import hash_password

# Configure the test client
client = TestClient(app)

# RapidAPI configuration
rapidapi_host = 'latest-mutual-fund-nav.p.rapidapi.com'
rapidapi_key = env.get("RAPIDAPI_KEY2")

# Database setup for testing
@pytest.fixture(scope="module")
def test_db():
    engine = create_engine("sqlite:///test.db")
    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    db = TestingSessionLocal()
    seed_test_data(db)
    db.close()

    yield  # Run tests

    Base.metadata.drop_all(bind=engine)

def seed_test_data(db):
    test_user = User(username="ravi kumar", password=hash_password("ravi kumar"))
    db.add(test_user)
    db.commit()
    db.refresh(test_user)

def authenticate():
    response = client.post("auth/login", json={
        "username": "ravi kumar",
        "password": "ravi kumar"
    })
    assert response.status_code == 200
    return response.json()["token"]

@pytest.fixture(scope="module")
def auth_token(test_db):
    token = authenticate()
    return token

def get_headers(auth_token):
    return {
        "Authorization": f"Bearer {auth_token}",
        "x-rapidapi-host": rapidapi_host,
        "x-rapidapi-key": rapidapi_key,
    }

def test_get_funds_success(auth_token):
    headers = get_headers(auth_token)
    response = client.get("/funds/CAMS", headers=headers) 
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list) 

def test_get_latest_funds_success(auth_token):
    headers = get_headers(auth_token)
    response = client.get("/funds/latest/Axis Mutual Fund", headers=headers)  
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list) 

def test_purchase_fund_success(auth_token):
    headers = get_headers(auth_token)
    response = client.post("/funds/2/purchase", json={ 
        "schemeCode": 120437,
        "schemeName": "Axis Banking & PSU Debt Fund - Direct Plan - Daily IDCW",
        "amount": 1039.131
    }, headers=headers)

    assert response.status_code == 200
    assert response.json()["message"] == "Fund purchased successfully"

def test_fetch_portfolio_success(auth_token):
    headers = get_headers(auth_token)
    response = client.get("/funds/1/portfolio", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list) 

def test_sell_fund_not_found(auth_token):
    headers = get_headers(auth_token)
    response = client.post("/funds/1/sell", json={
        "schemeCode": 99999,
        "amount": 500
    }, headers=headers)
    assert response.status_code == 404
    assert "detail" in response.json()

def test_purchase_fund_negative_amount(auth_token):
    headers = get_headers(auth_token)
    response = client.post("/funds/2/purchase", json={ 
        "schemeCode": 120437,
        "schemeName": "Axis Banking & PSU Debt Fund - Direct Plan - Daily IDCW",
        "amount": -1000
    }, headers=headers)
    assert response.status_code == 400
    assert "detail" in response.json()
