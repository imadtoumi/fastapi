from fastapi import status, Depends, HTTPException, APIRouter
from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# Get all posts 
@router.get("/", response_model=List[schemas.Post])
def post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


# Get all posts of specific user
@router.get("/{user_id}", response_model=List[schemas.Post])
def get_posts(user_id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).filter(models.Post.user_id == user_id).all()
    if not posts:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No posts created yet")
    return posts


# Get posts by their Ids
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id : {id} does not exist")
    return post


# Create post
@router.post("/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(**post.dict())
    new_post.user_id = current_user.id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# Delete post
@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id : {id} doesn't exist")

    if post.first().user_id == current_user.id:         # To check if the post belongs to the user that wants to delete it
        post.delete(synchronize_session=False)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not autorized to perform requested action")


# Update post
@router.put("/{id}")
def update_post(id: int, post_data: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} doesn't exist")
    
    if post.user_id == current_user.id:             # To check if the post belongs to the user that wants to update it
        post_query.update(post_data.dict(), synchronize_session=False)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not autorized to perform requested action")
    
    return post