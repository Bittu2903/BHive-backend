from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware

from app.modules.auth import routes as auth_routes

load_dotenv()

app = FastAPI()

router = APIRouter()

app.include_router(
    auth_routes.router,
    prefix="/auth",
    tags=["authentication"],
    responses={404: {"description": "Not found"}},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)