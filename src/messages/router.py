from fastapi import APIRouter, Body, Form, HTTPException, Request, Depends, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.auth.models import User
from src.auth.base_config import current_user, fastapi_users
from src.auth.manager import get_user_manager
from fastapi_users import schemas
from src.user.router import get_users

router = APIRouter(
    prefix="/message",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="src/templates")

@router.post("/receive_message/{sender}/{recipient}")
async def receive_message(sender: int, recipient: int, body: dict = Body(...)):
    message = body.get("message")
    if message: 
        print(message)
    print(f"Received message from {sender} to {recipient}, {message}")