import httpx
import requests
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import (BaseUserManager, IntegerIDMixin, exceptions, models,
                           schemas)
from starlette.responses import Response

from src.auth.models import User
from src.auth.utils import get_user_db
from src.config import SECRET_AUTH, URL_LOGGER


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET_AUTH
    verification_token_secret = SECRET_AUTH

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        params = {
            "type": "INFO",
            "user_id": user.id,
            "message": f"User ID: {user.id} EMAIL: {user.email} NAME: {user.name} SURNAME: {user.surname} IP: {request.client.host} registered."
        }
        async with httpx.AsyncClient() as client:
            await client.get(URL_LOGGER, params=params)

    async def create(
            self,
            user_create: schemas.UC,
            safe: bool = False,
            request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user

    async def on_after_login(
            self,
            user: models.UP,
            request: Optional[Request] = None,
            response: Optional[Response] = None,
    ) -> None:
        params = {
            "type": "INFO",
            "user_id": user.id,
            "message": f"User ID: {user.id} EMAIL: {user.email} NAME: {user.name} SURNAME: {user.surname} IP: {request.client.host} has logged in."
        }
        async with httpx.AsyncClient() as client:
            await client.get(URL_LOGGER, params=params)
        return  # pragma: no cover


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
