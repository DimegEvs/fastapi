from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.auth.manager import get_user_manager
from fastapi_users import schemas
from src.user.router import get_users

router = APIRouter(
    prefix="",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="src/templates")

@router.get("/", name="home")
def get_base_page(request: Request):
    register_url = request.url_for("register")
    home_url = request.url_for("home")
    search_url = request.url_for("search")
    return templates.TemplateResponse("base.html", {"request": request, "home_url": home_url, "register_url": register_url, "search_url": search_url})

@router.get("/search", name="search")
def get_search_page(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})

@router.get("/register", name="register")
def get_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.get("/login", name="login")
def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
