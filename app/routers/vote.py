from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oauth2
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/votes",
    tags=["Vote"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(vote: schemas.VoteCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # finding post that user is trying to vote on
    post = db.query(models.Post).filter(models.Post.uuid == vote.post_uuid).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {vote.post_uuid} does not exist")
    # checking if user has already voted on post
    vote_query = db.query(models.Vote).filter(models.Vote.post_uuid == vote.post_uuid and
                                              models.Vote.user_uuid == current_user.uuid)
    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.email} has already voted on post {vote.post_uuid}")
        new_vote = models.Vote(post_uuid=vote.post_uuid, user_uuid=current_user.uuid)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}
