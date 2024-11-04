from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

class UserReqModel(BaseModel):
    """Model for user login request."""
    username: str
    password: str

class TokenReqModel(BaseModel):
    """Model for token request."""
    token: str
    source: str = ""

class TokenResponseModelWithUser(BaseModel):
    """Model for token response."""
    user_id: int
    token: str
    refresh_token: str
    expire_at: int

class TokenPayloadModel(BaseModel):
    """Model for the token payload."""
    username: str
    auth_time: int
    expire_at: int
