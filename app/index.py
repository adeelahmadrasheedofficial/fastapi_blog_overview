from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import Optional, List
from . import models, schemas, utils
from sqlalchemy.orm import Session
from .database import engine, get_db
from .routers import post, user, auth

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


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
# using fastapi decorator to create a route
@app.get("/")
async def root():
    return {"message": "Welcome To Homepage !!!"}


### Get Latest Post ###
#######################
@app.get("/posts/latest")
def get_latest_post():
    post = my_post[len(my_post)-1]
    return {"data": post}
