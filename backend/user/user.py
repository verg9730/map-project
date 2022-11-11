from fastapi import FastAPI
from fastapi import APIRouter

from starlette.requests import Request


router = APIRouter()

@router.get("/user", tags=['user'])
async def name(request: Request):
    user = request.session.get('user')
    if user:
        return user

"""
@router.get("/name", tags=['user'])
async def name(request: Request):
    user = request.session.get('user')
    if user:
        name = user['name']
        return name


@router.get('/email', tags=['user'])
async def email(request: Request):
    user = request.session.get('user')
    if user:
        email = user['email']
        return email
"""