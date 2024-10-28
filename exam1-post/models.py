from pydantic import BaseModel
from typing import Optional

class Post(BaseModel):
    id: int
    title: str
    content: str
    author: str

class User(BaseModel):
    username: str
    password: str
    email: str
