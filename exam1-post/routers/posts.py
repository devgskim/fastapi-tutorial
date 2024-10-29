from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from typing import List
from models import Post as PostModel

from database import SessionLocal, engine, get_db

from pydantic import BaseModel
from typing import Optional

import logging

router = APIRouter()
posts = []

# Pydantic 모델 정의
class Post(BaseModel):
    id: int
    title: str
    content: str
    author: str

class PostCreate(BaseModel):
    title: str
    content: str
    author: str    

@router.get("/", response_model=list[Post])  # 여기에 리스트로 응답 모델 정의
def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = db.query(PostModel).offset(skip).limit(limit).all()  # 게시물 조회
    return posts

@router.get("/{post_id}", response_model=Post)  # 특정 ID를 조회하는 엔드포인트
def read_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(PostModel).filter(PostModel.id == post_id).first()  # 특정 ID로 게시물 검색
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")  # 게시물 없을 시 404 오류
    return post

@router.post("/", response_model=Post, summary="create post", description="create post")
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    """
    Create an Post with all the information:

    - **title**: title
    - **content**: content
    - **author**: author
    """
    try:
        db_post = PostModel(title=post.title, content=post.content, author=post.author)
        # db_post = PostModel(id=post.id, title=post.title, content=post.content, author=post.author)
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        logging.info(f"Post created with ID: {db_post.id}")
        return db_post
    except Exception as e:
        logging.error("Error creating post", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

# @router.delete("/{post_id}")
# def delete_post(post_id: int):
#     for index, post in enumerate(posts):
#         if post.id == post_id:
#             del posts[index]
#             return {"message": "Post deleted"}
#     raise HTTPException(status_code=404, detail="Post not found")

@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(PostModel).filter(PostModel.id == post_id).first()
    print(post)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found (fail delete)")

    db.delete(post)
    db.commit()

    return {"message": "Post deleted successfully"}

