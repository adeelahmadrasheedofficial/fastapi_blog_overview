from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional

router = APIRouter(prefix="/posts", tags=["Posts"])


#### Get All Posts ####
#######################
@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10,
              skip: int = 0, search: Optional[str] = ""):
    # posts = db.query(models.Post).filter(models.Post.user_uuid == current_user.uuid).all()
    # adding query parameters to the route
    posts = db.query(models.Post).filter(models.Post.user_uuid == current_user.uuid, models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # print(posts)
    return posts


### Create new Post ###
#######################
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    # print(current_user.uuid)
    new_post = models.Post(user_uuid=current_user.uuid, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


#### Get Single Post ####
#######################
@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.uuid == id).first()
    if not post:
        # using FastAPI exception rather than below method
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} was not found!')
    if post.user_uuid != current_user.uuid:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action.")
    return post


#### Update a Post ####
#######################
# using existing post schema
@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.uuid == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} doesn't exists.")
    if post.user_uuid != current_user.uuid:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action.")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post


#### Delete a Post ####
#######################
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.uuid == str(id))

    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} doesn't exists.")

    if post.user_uuid != current_user.uuid:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action.")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
