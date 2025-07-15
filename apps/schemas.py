from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

    class Config:
        from_attributes = True

# Extending the PostBase model in the classes below to inherit the config we put in it without having to retype it
class Post(PostBase):
    pass


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr


class Login(BaseModel):
    email: EmailStr
    password: str