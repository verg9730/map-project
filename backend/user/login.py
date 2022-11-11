import json

from fastapi import FastAPI
from fastapi import APIRouter

from starlette.config import Config
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse, RedirectResponse
from fastapi import APIRouter

from authlib.integrations.starlette_client import OAuth, OAuthError


router = APIRouter()

config = Config('/home/verg9730/map-project/backend/user/.env')
oauth = OAuth(config)

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@router.get("/login", tags=['login'])
async def homepage(request: Request):
    user = request.session.get('user')
    if user:
        data = json.dumps(user)
        html = (
            f'<pre>{data}</pre>'
            '<a href="/logout">logout</a>'
        )
        return HTMLResponse(html)
    return HTMLResponse('<a href="/login/google">login</a>')


@router.get('/login/google', tags=['login'])
async def login_via_google(request: Request):
    redirect_uri = 'http://34.125.39.187.nip.io:8000/auth/google'
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get('/auth/google', tags=['login'])
async def auth_via_google(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')
    user = token.get('userinfo')
    if user:
        request.session['user'] = dict(user)
    return RedirectResponse(url='/login')


@router.get('/logout',tags=['login'])
async def logout(request: Request):
    request.session.pop('user', None)   
    return RedirectResponse(url='/login')