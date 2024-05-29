from typing import Optional

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from src.auth.base_config import fastapi_users
from src.auth.models import User
from src.pages.utils import get_error_page

# Создание роутера для страниц с префиксом "" и тегом "Pages"
router = APIRouter(
    prefix="",
    tags=["Pages"]
)

# Инициализация шаблонов Jinja2 с указанием директории шаблонов
templates = Jinja2Templates(directory="src/templates")

# Определение текущего пользователя, допускающего необязательность авторизации
current_optional_user = fastapi_users.current_user(optional=True)

# Обработчик для главной страницы
@router.get("/", name="home")
def get_base_page(request: Request, user: User = Depends(current_optional_user)):
    user_info = None
    if user:
        user_info = user  # Получение информации о пользователе, если он авторизован
    register_url = request.url_for("register")  # URL для страницы регистрации
    home_url = request.url_for("home")  # URL для главной страницы
    search_url = request.url_for("search")  # URL для страницы поиска
    account_url = request.url_for("account")  # URL для страницы аккаунта
    return templates.TemplateResponse("index.html", {"request": request,
                                                    "home_url": home_url,
                                                    "register_url": register_url,
                                                    "search_url": search_url,
                                                    "account_url": account_url,
                                                    "user_info": user_info})  # Возвращение шаблона с параметрами

# Обработчик для страницы поиска
@router.get("/search", name="search")
def get_search_page(request: Request, user: User = Depends(current_optional_user)):
    user_info = None
    if user:
        user_info = user  # Получение информации о пользователе, если он авторизован
    else:
        error = get_error_page(request=request, user=user_info, error_message="Ошибка: Войдите в аккаунт")  # Возвращение страницы с ошибкой, если пользователь не авторизован
        return error
    return templates.TemplateResponse("search.html", {"request": request, "user_info": user_info})  # Возвращение шаблона с параметрами

# Обработчик для страницы регистрации
@router.get("/register", name="register")
def get_register_page(request: Request, user: User = Depends(current_optional_user)):
    user_info = None
    if user:
        user_info = user  # Получение информации о пользователе, если он авторизован
    return templates.TemplateResponse("register.html", {"request": request, "user_info": user_info})  # Возвращение шаблона с параметрами

# Обработчик для страницы входа
@router.get("/login", name="login")
def get_login_page(request: Request, user: User = Depends(current_optional_user)):
    user_info = None
    if user:
        user_info = user  # Получение информации о пользователе, если он авторизован
    return templates.TemplateResponse("login.html", {"request": request, "user_info": user_info})  # Возвращение шаблона с параметрами

# Обработчик для страницы аккаунта
@router.get("/account", name="account")
def get_account_page(request: Request, user: User = Depends(current_optional_user)):
    user_info = None
    if user:
        user_info = user  # Получение информации о пользователе, если он авторизован
    else:
        error = get_error_page(request=request, user=user_info, error_message="Ошибка: Войдите в аккаунт")  # Возвращение страницы с ошибкой, если пользователь не авторизован
        return error
    return templates.TemplateResponse("account.html", {"request": request, "user_info": user_info})  # Возвращение шаблона с параметрами

# Обработчик для страницы чата с определенным пользователем
@router.get("/chat/{user_id}")
def get_chat_page(request: Request, user_id: Optional[int] = None, user: User = Depends(current_optional_user)):
    user_info = None
    if user:
        user_info = user  # Получение информации о пользователе, если он авторизован
    else:
        error = get_error_page(request=request, user=user_info, error_message="Ошибка: Войдите в аккаунт")  # Возвращение страницы с ошибкой, если пользователь не авторизован
        return error

    return templates.TemplateResponse("chat.html", {"request": request, "user_info": user_info})  # Возвращение шаблона с параметрами

# Обработчик для страницы чата без указания пользователя
@router.get("/chat")
def get_chat_page(request: Request, user: User = Depends(current_optional_user)):
    user_info = None
    if user:
        user_info = user  # Получение информации о пользователе, если он авторизован
    else:
        error = get_error_page(request=request, user=user_info, error_message="Ошибка: Войдите в аккаунт")  # Возвращение страницы с ошибкой, если пользователь не авторизован
        return error
    error = get_error_page(request=request, user=user_info, error_message="Ошибка: Не выбран чат с пользователем")  # Возвращение страницы с ошибкой, если не выбран пользователь для чата
    return error

# Обработчик для страницы личных данных
@router.get("/personal-data")
def get_personal_data_page(request: Request, user_id: Optional[int] = None, user: User = Depends(current_optional_user)):
    user_info = None
    if user:
        user_info = user  # Получение информации о пользователе, если он авторизован
    return templates.TemplateResponse("personal.html", {"request": request, "user_info": user_info})  # Возвращение шаблона с параметрами

# Обработчик для страницы политики конфиденциальности
@router.get("/policy")
def get_policy_page(request: Request, user_id: Optional[int] = None, user: User = Depends(current_optional_user)):
    user_info = None
    if user:
        user_info = user  # Получение информации о пользователе, если он авторизован
    return templates.TemplateResponse("policy.html", {"request": request, "user_info": user_info})  # Возвращение шаблона с параметрами
