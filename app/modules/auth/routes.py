from fastapi import APIRouter, Request
from app.modules.auth.models import TokenResponseModel, UserReqModel
from app.modules.auth.operations import AuthModule

router = APIRouter()

@router.post("/login")
async def login_for_access_token(user: UserReqModel, request: Request):
    """
    Endpoint for user login to obtain an access token.

    Args:
        user (UserReqModel): User credentials containing username and password.
        request (Request): The HTTP request object.

    Returns:
        TokenResponseModel: A model containing the access token, refresh token, and expiration time.
    """
    module = AuthModule(user.username, user.password, request=request)
    token, expire_time = await module.login(user)
    return TokenResponseModel(
        token=token,
        refresh_token="",  # Currently not implemented, but can be added in the future
        expire_at=expire_time
    )
