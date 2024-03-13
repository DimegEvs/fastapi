import time
from typing import List

from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.manager import get_user_manager

from fastapi_users import schemas
from src.auth.models import user, User
from src.auth.base_config import current_user
from src.database import get_async_session

router = APIRouter(
    prefix=("/user"),
    tags=["users"]
)

@router.get("/get-all")
async def get_users(
        data: str,
        current_user_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(user.c.id, user.c.name, user.c.surname, user.c.email).where((user.c.name.like("%" + data + "%"))|
                                   user.c.surname.like("%" + data + "%"))
        result = await session.execute(query)
        users = result.mappings().all()
        users = [user for user in users if user.id != current_user_id]
        return users
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })

@router.get("/get_current_user/{user_id}")
async def get_current_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(user.c.id, user.c.name, user.c.surname, user.c.email).where(user.c.id == user_id)
        result = await session.execute(query)
        return result.mappings().all()
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })
        
