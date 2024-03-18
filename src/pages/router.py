from typing import Optional
from fastapi import APIRouter, Body, Form, HTTPException, Request, Depends, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.pages.utils import get_error_page
from src.auth.models import User
from src.auth.base_config import current_user, fastapi_users
from src.auth.manager import get_user_manager
from fastapi_users import schemas
from src.user.router import get_users
from src.user.router import get_current_user

router = APIRouter(
    prefix="",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="src/templates")

current_optional_user = fastapi_users.current_user(optional=True)

@router.get("/", name="home")
def get_base_page(request: Request, user: User = Depends(current_optional_user)):
    user_info = None
    if user:
        user_info = user
    register_url = request.url_for("register")
    home_url = request.url_for("home")
    search_url = request.url_for("search")
    account_url = request.url_for("account")
    return templates.TemplateResponse("base.html", {"request": request, 
                                                    "home_url": home_url, 
                                                    "register_url": register_url, 
                                                    "search_url": search_url, 
                                                    "account_url": account_url, 
                                                    "user_info": user_info})

@router.get("/search", name="search")
def get_search_page(request: Request, user: User = Depends(current_optional_user)):
    user_info = None
    if user:
        user_info = user
    else:
        error = get_error_page(request=request, user=user_info, error_message="Ошибка: Войдите в аккаунт")
        return error
    return templates.TemplateResponse("search.html", {"request": request, "user_info": user_info})

@router.get("/register", name="register")
def get_register_page(request: Request, user: User = Depends(current_optional_user)):
    user_info = None
    if user:
        user_info = user
    return templates.TemplateResponse("register.html", {"request": request, "user_info": user_info})

@router.get("/login", name="login")
def get_login_page(request: Request, user: User = Depends(current_optional_user)):
    user_info = None
    if user:
        user_info = user
    return templates.TemplateResponse("login.html", {"request": request, "user_info": user_info} )

@router.get("/account", name="account")
def get_account_page(request: Request, user: User = Depends(current_optional_user)):
    user_info = None
    if user:
        user_info = user
    else:
        error = get_error_page(request=request, user=user_info, error_message="Ошибка: Войдите в аккаунт")
        return error
    return templates.TemplateResponse("account.html", {"request": request, "user_info": user_info})

@router.get("/chat/{user_id}")
def get_chat_page(request: Request, user_id: Optional[int] = None, user: User = Depends(current_optional_user)):
    user_info = None
    if user:
        user_info = user
    else:
        error = get_error_page(request=request, user=user_info, error_message="Ошибка: Войдите в аккаунт")
        return error

    return templates.TemplateResponse("chat.html", {"request": request, "user_info": user_info})

@router.get("/chat")
def get_chat_page(request: Request, user: User = Depends(current_optional_user)):
    user_info = None
    if user:
        user_info = user
    else:
        error = get_error_page(request=request, user=user_info, error_message="Ошибка: Войдите в аккаунт")
        return error
    error = get_error_page(request=request, user=user_info, error_message="Ошибка: Не выбран чат с пользователем")
    return error