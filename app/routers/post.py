from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)



#### Get All Posts ####
#######################
@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


### Create new Post ###
#######################
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, 
                 db: Session = Depends(get_db), 
                 user_id: int = Depends(oauth2.get_current_user)
                 ):
    print(user_id)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


#### Get Single Post ####
#######################
@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int,  db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.uuid == id).first()
    if not post:
    # using FastAPI exception rather than below method
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f'post with id: {id} was not found!'
        )
    return post


#### Update a Post ####
#######################
#using existing post schema
@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, 
                db: Session = Depends(get_db),
                user_id: int = Depends(oauth2.get_current_user)
                ):
    post_query = db.query(models.Post).filter(models.Post.uuid == id)
    post = post_query.first()
    if post == None:        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} doesn't exists.")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post


#### Delete a Post ####
#######################
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,  db: Session = Depends(get_db),
                user_id: int = Depends(oauth2.get_current_user)
                ):
    post = db.query(models.Post).filter(models.Post.uuid == str(id))
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Post with id: {id} doesn't exists.")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
