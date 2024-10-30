from pydantic import BaseModel

class UserReqModel(BaseModel):
    username: str
    password: str

class TokenResModel(BaseModel):
    access_token: str
    token_type: str

class TokenPayloadModel(BaseModel):
    username: str
    auth_time: int
    expire_at: int