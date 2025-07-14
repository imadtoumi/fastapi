from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts", response_model=List[schemas.Post])
def post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id : {id} does not exist")
    return post


@app.post("/posts", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def post(post: schemas.Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id : {id} doesn't exist")
    post.delete(synchronize_session=False)
    db.commit()
    return post


@app.put("/posts/{id}")
def update_post(id: int, post_data: schemas.Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} doesn't exist")
    post_query.update(post_data.dict(), synchronize_session=False)
    db.commit()
    return post

@app.post("/users", response_model=schemas.UserOut ,status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate , db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)  # We has the password in here
    user.password = hashed_password         # We replace the old unhashed password with the new hashed one
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    print(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} does not exist")
    
    return user


@app.get("/test/{id}", response_model=schemas.UserOut)
def test(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User doesnt exist with id : {id}")

    return user

@app.post("/usertest", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def createtest(user_create: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user_create.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
