from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.auth.base_config import auth_backend, fastapi_users

from src.pages.router import router as router_pages
from src.auth.schemas import UserRead, UserCreate

app = FastAPI(
    title="App"
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
