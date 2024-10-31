from fastapi import FastAPI, Depends
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware

from app.helpers.auth import introspect_bearer_token
from app.modules.auth import routes as auth_routes
from app.modules.funds import routes as funds_routes

# Load environment variables from a .env file
load_dotenv()

app = FastAPI()

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include Auth Module Routes
app.include_router(
    auth_routes.router,
    prefix="/auth",
    tags=["authentication"],
    responses={404: {"description": "Not found"}},
)

# Include Funds Module Routes
app.include_router(
    funds_routes.router,
    prefix="/funds",
    tags=["funds"],
    dependencies=[Depends(introspect_bearer_token)],  # Protect these routes with token validation
    responses={404: {"description": "Not found"}},
)
