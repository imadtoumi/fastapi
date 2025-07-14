from fastapi import status, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Create user 
@router.post("/", response_model=schemas.UserOut ,status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate , db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)  # We has the password in here
    user.password = hashed_password         # We replace the old unhashed password with the new hashed one
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Get user by their Ids
@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    print(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} does not exist")
    
    return user

# Delete users by their Ids
@router.delete("/{id}")
def  delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if user.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id : {id} does not exits")
    user.delete(synchronize_session=False)
    db.commit()
    return status.HTTP_200_OK