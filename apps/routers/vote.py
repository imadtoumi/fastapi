from fastapi import Depends, status, APIRouter, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, oauth2

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/")
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id)
    found_vote = vote_query.first()
    if not post_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post you want to vote on Doesn't exist")
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Vote already placed")
        new_vote = models.Votes(post_id = vote.post_id, user_id = current_user.id) 
        db.add(new_vote)
        db.commit()
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote doesn't exist")

        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Post unvoted"}
    