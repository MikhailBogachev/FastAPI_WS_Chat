from fastapi import APIRouter, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.schemas import UserAuthSchema, UserRegisterSchema
from app.users.dao import UserDAO
from app.exceptions import UserAlreadyExistsException, PasswordMismatchException, IncorrectEmailOrPasswordException

router = APIRouter(prefix='/auth', tags=['Auth'])
templates = Jinja2Templates(directory='app/templates')


@router.post('/register/')
async def register_user(user_data: UserRegisterSchema):
    user = await UserDAO.find_one_or_none(email=user_data.email)
    if user:
        raise UserAlreadyExistsException
    if user_data.password != user_data.password_check:
        raise PasswordMismatchException

    hashed_password = get_password_hash(user_data.password)
    await UserDAO.add(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_password
    )

    return {'message': 'Вы успешно зарегистрированы!'}


@router.post('/login/')
async def auth_user(response: Response, user_data: UserAuthSchema):
    user = await authenticate_user(email=user_data.email, password=user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({'sub': user.id})
    response.set_cookie(key='user_access_token', value=access_token, httponly=True)
    return {'ok': True, 'access_token': access_token, 'refresh_token': None, 'message': 'Авторизация успешна!'}


@router.post('/logout/')
async def logout_user(response: Response):
    response.delete_cookie(key='users_access_token')
    return {'message': 'Пользователь успешно вышел из системы'}


@router.get('/', response_class=HTMLResponse, summary='Страница авторизации')
async def get_categories(request: Request):
    return templates.TemplateResponse('auth.html', {"request": request})
