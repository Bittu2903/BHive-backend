
from fastapi import APIRouter, Depends, HTTPException, Header, Request
from fastapi.security import OAuth2PasswordRequestForm
from app.modules.auth.models import UserReqModel
from app.modules.auth.operations import AuthModule
# from app.modules.auth.models import TokenModel


router = APIRouter()

@router.post("/login")
async def login_for_access_token(user: UserReqModel, request: Request):
    module = AuthModule(user.username, user.password, request=request)
    login_token = await module.login(user)
    return login_token

@router.get("/funds")
async def get_funds(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=403, detail="Authorization header missing")
    # Extracting the token from the Authorization header
    token = authorization.split(" ")[1]  # I'm assuming the format is "Bearer <token>"    
    module = AuthModule()
    get_funds = await module.get_funds(token)
    return get_funds
