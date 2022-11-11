import json
import models

from login import login

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

app.include_router(login.router)
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


@app.get("/getuser")
async def get_user(db:Session=Depends(get_db)):
    return db.query(models.User).all()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="10.182.0.2", port=8000, reload=True)
    # For login, please use 
    # http://34.125.39.187.nip.io:8000