from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.exceptions import TokenExpiredException, TokenNoFoundException


app = FastAPI()
app.mount('/static', StaticFiles(directory='app/static'), name='static')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_crendetials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# app.include_router(users_router)
# app.include_router(chat_router)


@app.get('/')
async def redirect_to_auth():
    return RedirectResponse(url='/auth')


@app.exception_handler(TokenExpiredException)
async def token_expired_exception_handler(request: Request, exc: HTTPException):
    return RedirectResponse(url='/auth')


@app.exception_handler(TokenNoFoundException)
async def token_no_found_exception_handler(request: Request, exc: HTTPException):
    return RedirectResponse('/auth')
