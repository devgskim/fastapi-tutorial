from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from starlette.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from passlib.context import CryptContext
import logging

# from schemas import UserCreate, Token
# from auth.jwt import create_access_token
# from auth.oauth2 import get_current_user
from database import engine, get_db, Base

from routers.posts import router as posts_router
from routers.users import router as users_router


# 로깅 설정
logging.basicConfig(level=logging.INFO)  # 로그 레벨 설정 (DEBUG, INFO, WARNING, ERROR, CRITICAL)

app = FastAPI(
    title="fastapi tutorial",
    summary="fastapi tutorial post, user",
    version="0.0.1"
)
app.include_router(posts_router, prefix="/posts", tags=["posts"])
app.include_router(users_router, prefix="/users", tags=["users"])  # 사용자 라우터 등록
# origins = [
#     "http://127.0.0.1:8000",
# ]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

@app.get("/")
def read_root():
    print("call main")
    return {"message": "Welcome to the Blog API"}


import argparse
if __name__ == '__main__':
    # Argument parser 설정
    parser = argparse.ArgumentParser(description='post application')
    parser.add_argument('--dbcreate', action='store_true', help='Create the database tables')

    args = parser.parse_args()
    if args.dbcreate:
        import database
        database.init_db()
        logging.info("create database")
    else:
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
        pass