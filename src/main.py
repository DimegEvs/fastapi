import requests
import redis.asyncio as redis
import httpx
from fastapi import Depends, FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from src.auth.models import User
from src.auth.base_config import auth_backend, fastapi_users
from src.config import URL_LOGGER

from src.pages.router import router as router_pages
from src.auth.schemas import UserRead, UserCreate
from src.user.router import router as router_user
from src.auth.base_config import current_user
from src.sub.router import router as router_sub
from src.config import URL_MIDDLEWARE

app = FastAPI(
    title="App"
)
@app.on_event("startup")
async def startup():
    redis_connection = redis.from_url("redis://my-redis-container", encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis_connection)

app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
    dependencies=[Depends(RateLimiter(times=100, seconds=60))]
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
    dependencies=[Depends(RateLimiter(times=100, seconds=60))]
)

app.include_router(router_pages, dependencies=[Depends(RateLimiter(times=100, seconds=60))])
app.include_router(router_user, dependencies=[Depends(RateLimiter(times=100, seconds=60))])
app.include_router(router_sub, dependencies=[Depends(RateLimiter(times=100, seconds=60))])

@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Логирование информации о запросе

    params = {
        "message": f"Request: {request.method} {request.url} IP: {request.client.host} HEADERS: {request.headers} COOKIES: {request.cookies}"
    }
    async with httpx.AsyncClient() as client:
        try:
            response1 = await client.get(URL_MIDDLEWARE, params=params)
        except httpx.HTTPError as e:
            print(f"HTTP error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    response = await call_next(request)
    return response
