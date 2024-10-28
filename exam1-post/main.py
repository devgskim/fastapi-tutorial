# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"message": "Hello World"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str = None):
#     return {"item_id": item_id, "q": q}

# @app.post("/items/")
# def create_item(item: dict):
#     return {"item_name": item.get("name"), "item_price": item.get("price")}

####################################################
# from fastapi import FastAPI
# from routers import items

# app = FastAPI()

# app.include_router(items.router)

# @app.get("/")
# def read_root():
#     return {"message": "Hello World"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)




from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext

from models import User
from schemas import UserCreate, Token
from database import engine, get_db, Base
from auth.jwt import create_access_token
from auth.oauth2 import get_current_user

from routers.posts import router as posts_router


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()
app.include_router(posts_router, prefix="/posts", tags=["posts"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Blog API"}

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

@app.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# @app.get("/users/me/", response_model=schemas.User)
# def read_users_me(current_user: User = Depends(get_current_user)):
#     return current_user