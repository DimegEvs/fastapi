import requests
from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from src.auth.models import User
from src.auth.base_config import auth_backend, fastapi_users
from src.config import URL_LOGGER

from src.pages.router import router as router_pages
from src.auth.schemas import UserRead, UserCreate
from src.user.router import router as router_user
from src.auth.base_config import current_user
from src.messages.router import router as router_message
from src.sub.router import router as router_sub

app = FastAPI(
    title="App",
    docs_url=None,
    redoc_url=None
)

app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_pages)
app.include_router(router_user)
app.include_router(router_message)
app.include_router(router_sub)
