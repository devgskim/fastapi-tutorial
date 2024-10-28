from fastapi import APIRouter, HTTPException
from typing import List
from models import Post

router = APIRouter()
posts = []

@router.post("/", response_model=Post)
def create_post(post: Post):
    posts.append(post)
    return post

@router.post("/", response_model=Post)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    db_post = PostModel(title=post.title, content=post.content, author=post.author)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post




@router.get("/", response_model=List[Post])
def read_posts():
    return posts

@router.get("/{post_id}", response_model=Post)
def read_post(post_id: int):
    for post in posts:
        if post.id == post_id:
            return post
    raise HTTPException(status_code=404, detail="Post not found")

@router.delete("/{post_id}")
def delete_post(post_id: int):
    for index, post in enumerate(posts):
        if post.id == post_id:
            del posts[index]
            return {"message": "Post deleted"}
    raise HTTPException(status_code=404, detail="Post not found")
