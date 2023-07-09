from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import Optional, List
from . import models, schemas
from sqlalchemy.orm import Session
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


my_post = [{"title": "title of my post", "content": "content of my post", "id": 1},
{"title": "title of my fav post", "content": "content of fav post", "id": 2}]

##### Find a Post #####
####### METHOD ########
# itterate to find post with id
def find_post(id):
    for p in my_post:
        if p["id"] == id:
            return p


## Find Index of Post ##
########################
def find_index_post(id):
    for i, p in enumerate(my_post):
        if p['id'] == id:
            return i

# using fastapi decorator to create a route
@app.get("/")
async def root():
    return {"message": "Welcome To Homepage !!!"}


#### Get All Posts ####
#######################
@app.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


### Create new Post ###
#######################
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


### Get Latest Post ###
#######################
@app.get("/posts/latest")
def get_latest_post():
    post = my_post[len(my_post)-1]
    return {"data": post}


#### Get Single Post ####
#######################
@app.get("/posts/{id}", response_model=schemas.PostResponse)
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
@app.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
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
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,  db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.uuid == str(id))
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Post with id: {id} doesn't exists.")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


