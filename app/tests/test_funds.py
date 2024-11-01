import pytest
from fastapi.testclient import TestClient
from app.helpers import env
from app.main import app 

client = TestClient(app)

rapidapi_host = 'latest-mutual-fund-nav.p.rapidapi.com'
rapidapi_key = env.get("RAPIDAPI_KEY")

def authenticate():
    response = client.post("auth/login", json={
        "username": "bhive_user",
        "password": "bhive_backend_secret_password"
    })
    assert response.status_code == 200
    return response.json()["token"]

@pytest.fixture(scope="module")
def auth_token():
    token = authenticate()
    return token

def get_headers(auth_token):
    return {
        "Authorization": f"Bearer {auth_token}",
        "x-rapidapi-host": rapidapi_host,
        "x-rapidapi-key": rapidapi_key,
    }

# TODO: To be tested (cannot test due to monthly quota exceed)

# def test_get_funds_success(auth_token):
#     headers = get_headers(auth_token)
#     response = client.get("/funds/CAMS", headers=headers) 
#     assert response.status_code == 200
#     data = response.json()
#     assert isinstance(data, list) 

# def test_get_latest_funds_success(auth_token):
#     headers = get_headers(auth_token)
#     response = client.get("/funds/latest/Axis Mutual Fund", headers=headers)  
#     assert response.status_code == 200
#     data = response.json()
#     assert isinstance(data, list) 

def test_purchase_fund_success(auth_token):
    headers = get_headers(auth_token)
    response = client.post("/funds/purchase", json={
        "schemeCode": 120437,
        "schemeName": "Axis Banking & PSU Debt Fund - Direct Plan - Daily IDCW",
        "amount": 1039.131
    }, headers=headers)

    assert response.status_code == 200


def test_purchase_fund_invalid_scheme(auth_token):
    headers = get_headers(auth_token)
    response = client.post("/funds/purchase", json={
        "schemeCode": 99999,  # Invalid scheme code
        "schemeName": "Invalid Fund",
        "amount": 0  # 0 is invalid for amount
    }, headers=headers)
    assert response.status_code == 400
