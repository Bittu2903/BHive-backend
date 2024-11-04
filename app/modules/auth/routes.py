from fastapi import APIRouter, Request, HTTPException, status
from app.modules.auth.models import TokenResponseModelWithUser, UserReqModel, User
from app.modules.auth.operations import AuthModule
from app.helpers.database import SessionLocal
from passlib.context import CryptContext 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

@router.post("/login")
async def login_for_access_token(user: UserReqModel, request: Request):
    """
    Endpoint for user login to obtain an access token.
    """
    db = SessionLocal() 
    module = AuthModule(username=user.username, password=user.password, request=request, db=db)
    user_id, token, expire_time = await module.login()
    return TokenResponseModelWithUser(
        user_id=user_id,
        token=token,
        refresh_token="",
        expire_at=expire_time
    )

@router.post("/signup")
async def signup(user: UserReqModel):
    """
    Endpoint for user registration.
    """
    db = SessionLocal()
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists."
        )
    
    hashed_password = pwd_context.hash(user.password)

    # Create a new user
    new_user = User(username=user.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.close()

    return {"message": "User registered successfully."}
