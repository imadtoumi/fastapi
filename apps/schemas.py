from pydantic import BaseModel, EmailStr, conint
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

    class Config:
        from_attributes = True

class Post(PostBase):
    user_id: int
    created_at: datetime
    user: UserOut
    
class PostCreate(PostBase):
    pass

class PostOut(BaseModel):
    Post: Post
    votes: int
    

# Token models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None
    

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) # type: ignore