from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import user
from src.database import get_async_session
from src.sub.service import SubService

router = APIRouter(
    prefix="/user",
    tags=["users"]
)


@router.get("/get-all")
async def get_users(
        data: str,
        current_user_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    # try:
    query = select(user.c.id, user.c.name, user.c.surname, user.c.email).where((user.c.name.like("%" + data + "%")) |
                                                                               user.c.surname.like("%" + data + "%"))
    result = await session.execute(query)
    users = result.mappings().all()
    users_list = []
    for u in users:
        if u.id != current_user_id:
            u = dict(u)
            u['is_subscribed'] = await SubService.check_subscribe(current_user_id, u['id'])
            users_list.append(u)
    return users_list


# except Exception:
#     raise HTTPException(status_code=500, detail={
#         "status": "error",
#         "data": None,
#         "details": None
#     })

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
