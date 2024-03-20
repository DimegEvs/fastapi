import httpx
from fastapi import APIRouter, Body, Form, HTTPException, Request, Depends, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import and_, delete, insert, select

from src.config import URL_LOGGER
from src.database import get_async_session
from src.auth.models import User
from src.auth.base_config import current_user, fastapi_users
from src.auth.manager import get_user_manager
from fastapi_users import schemas
from src.user.router import get_users
from fastapi.exceptions import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from src.sub.models import sub

router = APIRouter(
    prefix="/sub",
    tags=["Sub"]
)

templates = Jinja2Templates(directory="src/templates")


@router.get("/get_sub_list/{user_id}")
async def get_list_sub(user_id: int, request: Request, session: AsyncSession = Depends(get_async_session)):
    query = select(sub.c.sub_id).where(sub.c.user_id == user_id)
    result = await session.execute(query)
    return result.mappings().all()


@router.post("/add_sub/{user_id}/{sub_id}")
async def add_sub(user_id: int, sub_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(sub).values(
            user_id=user_id,
            sub_id=sub_id
        )
        result = await session.execute(stmt)
        await session.commit()
        params = {
            "type": "INFO",
            "message": f"User ID: {user_id} subscribed on sub ID: {sub_id}"
        }
        async with httpx.AsyncClient() as client:
            await client.get(URL_LOGGER, params=params)
    except Exception as e:
        params = {
            "type": "ERROR",
            "message": f"User ID: {user_id} not sub on sub ID: {sub_id}, error"
        }
        async with httpx.AsyncClient() as client:
            await client.get(URL_LOGGER, params=params)


@router.get("/check_subscription/{user_id}/{sub_id}")
async def check_subscription(sub_id: int, user_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(sub).where(and_(sub.c.user_id == user_id, sub.c.sub_id == sub_id))
    result = await session.execute(query)
    return {
        "is_subscribed": result.mappings().first() is not None
    }


@router.get("/unsub/{user_id}/{sub_id}")
async def delete_sub(sub_id: int, user_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        delete_stmt = delete(sub).where(and_(sub.c.user_id == user_id, sub.c.sub_id == sub_id))
        result = await session.execute(delete_stmt)
        await session.commit()
        params = {
            "type": "INFO",
            "message": f"User ID: {user_id} unsubscribed on sub ID: {sub_id}"
        }
        async with httpx.AsyncClient() as client:
            await client.get(URL_LOGGER, params=params)
        return {"status_code": 200}
    except Exception:
        raise HTTPException(status_code=500)
