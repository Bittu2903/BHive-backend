from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from app.helpers.time import current_time
from app.modules.auth.models import TokenReqModel
from app.modules.auth.operations import AuthModule

# Define the OAuth2 scheme for bearer token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def introspect_bearer_token(request: Request, token: str = Depends(oauth2_scheme)):
    """
    Validate the bearer token provided in the request.

    Args:
        request: The incoming HTTP request.
        token: The bearer token extracted from the request.

    Raises:
        HTTPException: If the token is expired or invalid.

    Returns:
        bool: True if the token is valid and not expired.
    """
    try:
        # Decode and validate the token
        user_data_from_login = AuthModule(model=TokenReqModel(token=token)).decode_safemeet_jwt_token()
        
        # Check if the token has expired
        if user_data_from_login.expire_at < current_time():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired.")

        return True
    except Exception as e:
        # Raise an HTTPException if the token is invalid
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Not Authorized: {str(e)}')
