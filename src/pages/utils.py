from fastapi import APIRouter, Body, Form, HTTPException, Request, Depends, status
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import Response
from src.auth.models import User
from math import ceil
from src.auth.base_config import fastapi_users
from starlette.status import HTTP_429_TOO_MANY_REQUESTS

current_optional_user = fastapi_users.current_user(optional=True)

templates = Jinja2Templates(directory="src/templates")


def get_error_page(request: Request, user, error_message: str = "Ошибка"):
    user_info = user
    return templates.TemplateResponse("error.html",
                                      {"request": request, "user_info": user_info, "error_message": error_message})


# async def http_default_callback(request: Request, response: Response, pexpire: int):
#     """
#     default callback when too many requests
#     :param request:
#     :param pexpire: The remaining milliseconds
#     :param response:
#     :return:
#     """
#     user_info = None
#     expire = ceil(pexpire / 1000)
#     return templates.TemplateResponse("error.html",
#                                       {"request": request, "user_info": user_info, "error_message": f"Слишком много запросов, попробуйте через {expire} секунд"})
