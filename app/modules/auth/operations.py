import os
import time
import jwt
from fastapi import APIRouter, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from app.helpers import env
from app.modules.auth.models import TokenPayloadModel, TokenReqModel

# Create a router instance
router = APIRouter()

# OAuth2 scheme for token retrieval
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dummy user credentials loaded from environment variables
DUMMY_USERNAME = env.get("DUMMY_USERNAME")
DUMMY_PASSWORD = env.get("DUMMY_PASSWORD")

# JWT constants
JWT_KEY: str = "2a07fd44070c3630b86e2997febe3665e53eb729f1fa5aeb9999b8b9b84e4177"
JWT_ALGORITHM = "HS256"
ONE_DAY = 86400  # 24 hours in seconds

class AuthModule:
    def __init__(self, model: TokenReqModel = None, username: str = None, password: str = None, request: Request = None):
        """
        Initialize AuthModule with user credentials and request object.

        Args:
            model (TokenReqModel, optional): Token request model.
            username (str, optional): Username for authentication.
            password (str, optional): Password for authentication.
            request (Request, optional): The request object for context.
        """
        self.model = model
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
        return token, expire_time
    
    def decode_safemeet_jwt_token(self):
        """
        Decode a JWT token and return its payload.

        Raises:
            HTTPException: If the token is invalid or expired.
        """
        try:
            return TokenPayloadModel(**jwt.decode(self.model.token, JWT_KEY, algorithms=JWT_ALGORITHM))
        except Exception:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired access token.")

    async def login(self, form_data):
        """
        Authenticate a user and return a JWT token and its expiry time.

        Args:
            form_data: User credentials containing username and password.

        Returns:
            Tuple[str, int]: A tuple containing the JWT token and its expiry time.

        Raises:
            HTTPException: If authentication fails.
        """
        if form_data.username == DUMMY_USERNAME and form_data.password == DUMMY_PASSWORD:
            bearer_token, expiry_time = self.__generate_jwt_token__()
            return bearer_token, expiry_time
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
