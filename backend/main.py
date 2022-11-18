import json
import httpx
import models, schemas

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

@app.get("/")
async def hello():
    return "hello world!"

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()  

class access_token_form(BaseModel):
    accessToken : str
    expiresIn : str
    scope : str
    tokenType: str

URL = " https://www.googleapis.com/oauth2/v3/userinfo"

@app.post('/get_user_info/')
async def get_user_info(form : access_token_form):
    response = await get
    return form
    

@app.get("/users")
async def get_user(db:Session=Depends(get_db)):
    return db.query(models.User).all()

@app.get("/users/memos/{userid}")
async def get_user_memo(userid:int, db:Session=Depends(get_db)):
    my_user = db.query(models.User).filter(models.User.id == userid).first().memos
    return my_user

@app.get("/points")
async def get_point(db:Session=Depends(get_db)):
    return db.query(models.Point).all()

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

@app.get("/memos")
async def get_memo(db:Session=Depends(get_db)):
    return db.query(models.Memo).all()

@app.get("/memos/private")
async def get_memo(db:Session=Depends(get_db)):
    return db.query(models.Memo).filter(models.Memo.memo_type == "private").all()

@app.get("/memos/public")
async def get_memo(db:Session=Depends(get_db)):
    return db.query(models.Memo).filter(models.Memo.memo_type == "public").all()

@app.post("/memos/create")
async def create_memo(request:schemas.Memo, db:Session=Depends(get_db)):
    new_memo = models.Memo(user_id=request.user_id,point_id=request.point_id,memo_type=request.memo_type,memo_x=request.memo_x,memo_y=request.memo_y, memo_content=request.memo_content)
    db.add(new_memo)
    db.commit()
    db.refresh(new_memo)

    return new_memo






if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="10.182.0.2", port=8000, reload=True)
    # For login, please use 
    # http://34.125.39.187.nip.io:8000