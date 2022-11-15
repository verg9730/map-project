import json
import models
from fastapi import APIRouter
from fastapi import FastAPI, Depends
from starlette.config import Config
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from database import engine, SessionLocal
from authlib.integrations.starlette_client import OAuth, OAuthError
from sqlalchemy.orm import Session

# Set router
router = APIRouter()

# Google Auth Config
config = Config('/home/verg9730/map-project/backend/login/.env')
oauth = OAuth(config)

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# Connect this file & DB
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get("/login", tags=['login'])
async def homepage(request: Request, db:Session=Depends(get_db)):
    user = request.session.get('user')
    if user:
        data = json.dumps(user)
        html = (
            f'<pre>{data}</pre>'
            '<a href="/logout">logout</a>'
        )

        new_user = models.User(user_name=user['name'],user_email=user['email'])
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return user
    return HTMLResponse('<a href="/login/google">login</a>')


@router.get("/name", tags=['login'])
async def name(request: Request):
    user = request.session.get('user')
    if user:
        name = user['name']
        return user


@router.get('/email', tags=['login'])
async def email(request: Request):
    user = request.session.get('user')
    if user:
        email = user['email']
        return email


@router.get('/login/google', tags=['login'])
async def login_via_google(request: Request):
    user = request.session.get('user')
    if user:
        data = json.dumps(user)
        return user
    else :
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