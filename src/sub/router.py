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

from sqlalchemy.ext.asyncio import AsyncSession

from src.sub.models import sub

# Создание роутера для управления подписками с префиксом "/sub" и тегом "Sub"
router = APIRouter(
    prefix="/sub",
    tags=["Sub"]
)

# Инициализация шаблонов Jinja2 с указанием директории шаблонов
templates = Jinja2Templates(directory="src/templates")

# Определение текущего пользователя, допускающего необязательность авторизации
current_optional_user = fastapi_users.current_user(optional=True)

# Обработчик для получения списка подписок пользователя
@router.get("/get_sub_list/{user_id}")
async def get_list_sub(user_id: int, request: Request, session: AsyncSession = Depends(get_async_session),
                       user: User = Depends(current_optional_user)):
    if user.id == user_id:
        query = select(sub.c.sub_id).where(sub.c.user_id == user_id)  # Запрос для получения списка подписок пользователя
        result = await session.execute(query)  # Выполнение запроса
        return result.mappings().all()  # Возвращение результатов запроса
    else:
        raise HTTPException(status_code=500)  # Ошибка, если пользователь не авторизован

# Обработчик для добавления подписки
@router.post("/add_sub/{user_id}/{sub_id}")
async def add_sub(user_id: int, sub_id: int, session: AsyncSession = Depends(get_async_session),
                  user: User = Depends(current_optional_user)):
    if user.id == user_id:
        try:
            stmt = insert(sub).values(
                user_id=user_id,
                sub_id=sub_id
            )  # Вставка новой подписки в базу данных
            await session.execute(stmt)  # Выполнение вставки
            await session.commit()  # Коммит транзакции
            params = {
                "type": "INFO",
                "user_id": user_id,
                "message": f"User ID: {user_id} subscribed on sub ID: {sub_id}"
            }
            async with httpx.AsyncClient() as client:
                await client.get(URL_LOGGER, params=params)  # Логирование действия
        except Exception as e:
            params = {
                "type": "ERROR",
                "user_id": user_id,
                "message": f"User ID: {user_id} not sub on sub ID: {sub_id}, error"
            }
            async with httpx.AsyncClient() as client:
                await client.get(URL_LOGGER, params=params)  # Логирование ошибки
    else:
        raise HTTPException(status_code=500)  # Ошибка, если пользователь не авторизован

# Обработчик для проверки подписки пользователя
@router.get("/check_subscription/{user_id}/{sub_id}")
async def check_subscription(sub_id: int, user_id: int, session: AsyncSession = Depends(get_async_session),
                             user: User = Depends(current_optional_user)):
    if user.id == user_id:
        query = select(sub).where(and_(sub.c.user_id == user_id, sub.c.sub_id == sub_id))  # Запрос для проверки подписки
        result = await session.execute(query)  # Выполнение запроса
        return {
            "is_subscribed": result.mappings().first() is not None  # Проверка наличия подписки
        }
    else:
        raise HTTPException(status_code=500)  # Ошибка, если пользователь не авторизован

# Обработчик для удаления подписки
@router.get("/unsub/{user_id}/{sub_id}")
async def delete_sub(sub_id: int, user_id: int, session: AsyncSession = Depends(get_async_session),
                     user: User = Depends(current_optional_user)):
    if user.id == user_id:
        try:
            delete_stmt = delete(sub).where(and_(sub.c.user_id == user_id, sub.c.sub_id == sub_id))  # Запрос для удаления подписки
            await session.execute(delete_stmt)  # Выполнение удаления
            await session.commit()  # Коммит транзакции
            params = {
                "type": "INFO",
                "user_id": user_id,
                "message": f"User ID: {user_id} unsubscribed on sub ID: {sub_id}"
            }
            async with httpx.AsyncClient() as client:
                await client.get(URL_LOGGER, params=params)  # Логирование действия
            return {"status_code": 200}  # Возвращение статуса успешного выполнения
        except Exception:
            raise HTTPException(status_code=500)  # Ошибка при удалении подписки
    else:
        raise HTTPException(status_code=500)  # Ошибка, если пользователь не авторизован
