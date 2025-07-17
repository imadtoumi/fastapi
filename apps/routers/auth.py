from fastapi import HTTPException, APIRouter, status, Response, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils, oauth2

router = APIRouter(tags=["Authentication"]) 

# Why we are calling .username from user_creds even we have no username field in db ?
# Bc OAuth2PasswordRequestForm only return username and password in the dict object

@router.post("/login", response_model=schemas.Token)
def login(user_creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_creds.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
        
    if not utils.verify(user_creds.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    encoded_jwt = oauth2.create_access_token(data = {"user_id": user.id})

    return {"access_token": encoded_jwt, "token_type": "bearer"}