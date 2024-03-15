from fastapi import APIRouter, Body, Form, HTTPException, Request, Depends, status
from fastapi.templating import Jinja2Templates

from src.auth.models import User
from src.auth.base_config import fastapi_users

current_optional_user = fastapi_users.current_user(optional=True)

templates = Jinja2Templates(directory="src/templates")

def get_error_page(request: Request, user, error_message: str = "Ошибка"):
    user_info = user
    return templates.TemplateResponse("error.html", {"request": request, "user_info": user_info, "error_message": error_message})