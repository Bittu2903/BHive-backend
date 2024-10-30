import os
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends, HTTPException, status
from app.helpers import env
from app.modules.auth.models import TokenPayloadModel

from typing import Union
from fastapi import Request
from pydantic import BaseModel
import jwt
import time


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dummy user credentials
DUMMY_USERNAME = env.get("DUMMY_USERNAME")
DUMMY_PASSWORD = env.get("DUMMY_PASSWORD")

# Constants
JWT_KEY: str = "2a07fd44070c3630b86e2997febe3665e53eb729f1fa5aeb9999b8b9b84e4177"
JWT_ALGORITHM = "HS256"
ONE_DAY = 86400  # 24 hours in seconds

class AuthModule:
    def __init__(self, username: str = None, password: str = None, request: Request = None):
        self.username = username
        self.password = password
        self.request = request
    
    def __generate_token_expiry_time__(self) -> int:
        """Generate token expiry time (24 hours from now)."""
        return int(time.time()) + ONE_DAY
    
    def __generate_jwt_token__(self) -> str:
        """Generate JWT token."""
        expire_time = self.__generate_token_expiry_time__()
        payload = TokenPayloadModel(
            username=self.username,
            auth_time=int(time.time()),
            expire_at=expire_time
        )
        token = jwt.encode(payload.dict(), JWT_KEY, algorithm=JWT_ALGORITHM)
        return token

    async def login(self, form_data):
        print(form_data.username, DUMMY_USERNAME, form_data.password, DUMMY_PASSWORD)
        if form_data.username == DUMMY_USERNAME and form_data.password == DUMMY_PASSWORD:
            bearer_token =  self.__generate_jwt_token__()
            return bearer_token
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    async def get_funds(self, token: str = Depends(oauth2_scheme)):
        print("inside")
        # Placeholder for fetching funds
        return [{"fund": "HDFC", "scheme": "HDFC Equity Fund"}, {"fund": "ICICI", "scheme": "ICICI Balanced Fund"}]

