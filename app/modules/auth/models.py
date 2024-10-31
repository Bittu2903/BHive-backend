from pydantic import BaseModel

class UserReqModel(BaseModel):
    """Model for user login request."""
    username: str
    password: str

class TokenReqModel(BaseModel):
    """Model for token request."""
    token: str
    source: str = ""  # Optional source field for token request

class TokenResponseModel(BaseModel):
    """Model for token response."""
    token: str
    refresh_token: str
    expire_at: int  # Expiration time of the token in seconds

class TokenPayloadModel(BaseModel):
    """Model for the token payload."""
    username: str
    auth_time: int  # Time when the token was issued
    expire_at: int  # Expiration time of the token
