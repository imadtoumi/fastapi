from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Users models
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr

class Login(BaseModel):
    email: EmailStr
    password: str


# Posts models
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    created_at: datetime

    class Config:
        from_attributes = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    user_id: int
    user: UserOut


# Token models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None