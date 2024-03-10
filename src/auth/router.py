import time

from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.manager import get_user_manager

from fastapi_users import schemas
from src.auth.models import user
from src.auth.base_config import current_user
from src.database import get_async_session

router = APIRouter(
    prefix=("/user"),
    tags=["users"]
)

@router.get("")
async def get_users(
        data: str,
        session: AsyncSession = Depends(get_async_session),
):
    try:
        query = select(user).where((user.c.name.like("%" + data + "%"))|
                                   user.c.surname.like("%" + data + "%"))
        result = await session.execute(query)
        return {
            "status": "success",
            "data": result.all(),
            "details": None
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })
        
