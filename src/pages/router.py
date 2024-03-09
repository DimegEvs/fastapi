from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from src.auth.router import get_users

router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="src/templates")

@router.get("/base")
def get_base_page(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

@router.get("/search/{data}")
def get_search_page(request: Request, users=Depends(get_users)):
    print(users["data"])
    return templates.TemplateResponse("search.html", {"request": request, "users": users["data"]})