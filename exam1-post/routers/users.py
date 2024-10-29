from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError  # IntegrityError 추가

from passlib.context import CryptContext
from typing import List
from models import User as UserModel

from database import get_db

from pydantic import BaseModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 비밀번호 해싱 함수
def hash_password(plain_password: str):
    return pwd_context.hash(plain_password)

# 비밀번호 검증 함수
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)



router = APIRouter()
posts = []

# Pydantic 모델 정의
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # 비밀번호 해싱
    hashed_password = hash_password(user.password)
    db_user = UserModel(username=user.username, email=user.email, hashed_password=hashed_password)
    # db_user = UserModel(username=user.username, email=user.email, hashed_password=user.password)  # 비밀번호는 해싱해야 함
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:  # 중복 오류 처리
        db.rollback()  # 트랜잭션 롤백
        raise HTTPException(status_code=400, detail="Username or email already exists")

@router.get("/", response_model=list[UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    user_db = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user_db is None:
        raise HTTPException(status_code=404, detail="User not found")

    # 비밀번호 해싱
    user_db.username = user.username
    user_db.email = user.email
    user_db.hashed_password = hash_password(user.password)  # 새 비밀번호로 해싱
    # user_db.hashed_password = user.password  # 비밀번호는 해싱해야 함
    db.commit()
    db.refresh(user_db)
    return user_db

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
