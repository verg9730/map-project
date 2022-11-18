import requests
import json
import models, schemas
from geocoding import geocoding_reverse

# from login import login

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import engine, SessionLocal

from starlette.middleware.sessions import SessionMiddleware
from starlette.config import Config
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

app=FastAPI()

# app.include_router(login.router)
# app.include_router(user.router)
app.add_middleware(SessionMiddleware, secret_key="!secret")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

# @app.get("/")
# async def hello(request: Request):
#     user = request.session.get('user')
#     if user:
#         return "hello world!"
#     else:
#         return "You are not logged in!"

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()  

class access_token_form(BaseModel):
    access_token : str
    expires_in : int
    scope : str
    token_type: str

URL = "https://www.googleapis.com/oauth2/v3/userinfo"

@app.post('/sign_in')
async def sign_in(form : access_token_form, db:Session=Depends(get_db)):
    resp = requests.post(url=URL, data = dict(form))
    raw_user_info = dict(resp.json())
    existing_user = db.query(models.User).filter(models.User.user_name == raw_user_info['name']).filter(models.User.user_email == raw_user_info['email']).first()
    if existing_user:
        return existing_user
    else:
        new_user = models.User(user_name=raw_user_info["name"], user_email=raw_user_info["email"])
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        user = db.query(models.User).filter(models.User.user_name==raw_user_info["name"]).filter(models.User.user_email==raw_user_info["email"]).first()
        return user

# @app.get('/logout')
# async def logout(request: Request):
#     request.session.pop('user', None)
#     return RedirectResponse(url='/')

@app.get("/users")
async def get_all_users(db:Session=Depends(get_db)):
    return db.query(models.User).all()

@app.get("/users/memos/{userid}")
async def get_user_memo(userid:int, db:Session=Depends(get_db)):
    my_user = db.query(models.User).filter(models.User.id == userid).first().memos
    return my_user

@app.get("/points")
async def get_all_points(db:Session=Depends(get_db)):
    return db.query(models.Point).all()

# @app.get("/points/{point_id}")
# async def get_address(point_id:int, db:Session=Depends(get_db)):
#     point_x = db.query(models.Point).filter(models.Point.id == point_id).first().point_x
#     point_y = db.query(models.Point).filter(models.Point.id == point_id).first().point_y
 
#     coordinate = f"{point_x}, {point_y}"
#     address = geocoding_reverse(coordinate)
#     return {"postal code" : address[0].split(',')[-2].strip()}


class Coordinate(BaseModel):
    point_x : float
    point_y : float


@app.post("/points/postalcode")
async def get_postal_code(request:Coordinate, db:Session=Depends(get_db)):
    point_x = request.point_x
    point_y = request.point_y
 
    coordinate = f"{point_x}, {point_y}"
    postal_code = geocoding_reverse(coordinate)[0].split(',')[-2].strip()
    if not db.query(models.Point).filter(postal_code==postal_code).first():
        new_point = models.Point(postal_code=postal_code)
        db.add(new_point)
        db.commit()
        db.refresh(new_point)
    return postal_code #setPointid로 프론트에서 변수 설정하면 됨!

@app.get("/memos")
async def get_all_memos(db:Session=Depends(get_db)):
    return db.query(models.Memo).all()

@app.get("/memos/private/{user_id}")
async def get_private_memo(db:Session=Depends(get_db)):
    return db.query(models.Memo).filter(models.Memo.memo_type == "private").filter(models.Memo.user_id==user_id).all()

@app.get("/memos/public/{point_id}")
async def get_public_memo(point_id:int, db:Session=Depends(get_db)):
    return db.query(models.Memo).filter(models.Memo.memo_type == "public").filter(models.Memo.point_id==point_id).all()
    
@app.post("/memos/create")
async def create_memo(request:schemas.Memo, db:Session=Depends(get_db)):
    new_memo = models.Memo(user_id=request.user_id,point_id=request.point_id,memo_type=request.memo_type,memo_x=request.memo_x,memo_y=request.memo_y, memo_content=request.memo_content)
    db.add(new_memo)
    db.commit()
    db.refresh(new_memo)

    return new_memo

@app.delete("/memos/{memo_id}")
async def delete_memo(memo_id:int, db:Session=Depends(get_db)):
    memo = db.query(models.Memo).filter(models.Memo.id == memo_id).first()
    if memo:
        db.query(models.Memo).filter_by(id= memo_id).delete()
        db.commit()
        return {f"{memo_id} : deleted"}
    else:
        return {"no matching memo"}

@app.post("/points")
async def create_point(request:schemas.Point, db:Session=Depends(get_db)):
    new_point = models.Point(point_x=request.point_x,point_y=request.point_y,point_range=request.point_range)
    db.add(new_point)
    db.commit()
    db.refresh(new_point)
    return new_point

@app.delete("/points/{point_id}")
async def delete_point(point_id:int, db:Session=Depends(get_db)):
    point = db.query(models.Point).filter(models.Point.id == point_id).first()
    if point:
        db.query(models.Point).filter_by(id= point_id).delete()
        db.commit()
        return {f"{point_id} : deleted"}
    else:
        return {"no matching point"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="10.182.0.2", port=8000, reload=True)
    # For login, please use 
    # http://34.125.39.187.nip.io:8000