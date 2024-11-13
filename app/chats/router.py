from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.users.dao import UserDAO
from app.users.dependensies import get_current_user
from app.users.models import User


router = APIRouter(prefix='/chat', tags=['Chat'])
templates = Jinja2Templates(directory='app/templates')


@router.get('/', response_class=HTMLResponse, summary="Chat Page")
async def get_chat_page(
    request: Request,
    user_data: User = Depends(get_current_user)
):
    users_all = await UserDAO.find_all()
    return templates.TemplateResponse(
        'chat.html',
        {'request': request, 'user': user_data, 'users_all': users_all}
    )
