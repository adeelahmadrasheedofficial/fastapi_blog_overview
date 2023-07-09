# from fastapi import FastAPI, Response, status, HTTPException, Depends
# from fastapi.params import Body
# from typing import Optional
# from random import randrange
# from psycopg2.extras import RealDictCursor
# import psycopg2
# import time
# from . import models, schemas
# from sqlalchemy.orm import Session
# from .database import engine, get_db

# models.Base.metadata.create_all(bind=engine)

# app = FastAPI()


# while True:
#     try: 
#         conn = psycopg2.connect(host='localhost', database='fastapi_db', user='postgres', password='admin1122', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connection was successfull.')
#         break
#     except Exception as e:
#         print(f'Unable to establish database connection: {e}')
#         time.sleep(5)
        

# my_post = [{"title": "title of my post", "content": "content of my post", "id": 1},
# {"title": "title of my fav post", "content": "content of fav post", "id": 2}]

# # using fastapi decorator to create a route
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


# #### Get All Posts ####
# #######################
# @app.get("/posts")
# def get_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     # cursor.execute("""SELECT * FROM posts""")
#     # posts = cursor.fetchall()
#     return {"data": posts}


# ### Create new Post ###
# #######################
# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
#     # using sqlalchemy ORM
#     # More effiecient way
#     new_post = models.Post(**post.dict())
#     # new_post = models.Post(title=post.title,
#     #                        content=post.content,
#     #                        published=post.published)
    
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     return {"data": new_post}

# # def create_posts(post: Post):
#     # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
#     # (post.title, post.content, post.published))
#     # new_post = cursor.fetchone()
#     # conn.commit()

#     # # changing pydantic model to dict
#     # post_dict = post.dict()
#     # # assigning a random id to post dictionary
#     # post_dict['id'] = randrange(0, 100000)
#     # my_post.append(post_dict)
#     # return {"data": post_dict}
#     # return {"data": new_post}


# ##### Find a Post #####
# ####### METHOD ########
# # itterate to find post with id
# def find_post(id):
#     for p in my_post:
#         if p["id"] == id:
#             return p


# ## Find Index of Post ##
# ########################
# def find_index_post(id):
#     for i, p in enumerate(my_post):
#         if p['id'] == id:
#             return i


# ### Get Latest Post ###
# #######################
# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_post[len(my_post)-1]
#     return {"data": post}


# #### Get Single Post ####
# #######################
# @app.get("/posts/{id}")
# def get_post(id: int,  db: Session = Depends(get_db)):
#     post = db.query(models.Post).filter(models.Post.uuid == str(id)).first()

# # def get_post(id: int):
# #     cursor.execute("""SELECT * FROM posts WHERE uuid = %s""", (str(id),))
# #     post = cursor.fetchone()
# #     print(post)
# #     post = find_post(id)
#     if not post:
#     # using FastAPI exception rather than below method
#         raise HTTPException(
#             status.HTTP_404_NOT_FOUND,
#             detail=f'post with id: {id} was not found!'
#         )
#     return {"data": post}

#         # #changing status code of response
#         # # response.status_code = 404
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {"message": f'post with "{id}" was not found!'}


# #### Delete a Post ####
# #######################
# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int,  db: Session = Depends(get_db)):
#     post = db.query(models.Post).filter(models.Post.uuid == str(id))
#     if post.first() == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                     detail=f"Post with id: {id} doesn't exists.")
#     post.delete(synchronize_session=False)
#     db.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)



# # def delete_post(id: int):
# #     cursor.execute("""DELETE FROM posts WHERE uuid = %s RETURNING *""",(str(id),))
# #     deleted_post = cursor.fetchone()
# #     conn.commit()
#     # if post == None:    
#     # # find the index in the  array that has required id
#     # index = find_index_post(id)
#     # if index == None or not index:
#         # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#         #                     detail=f"Post with id: {id} doesn't exists.")
#     # my_post.pop(index)
#     # return Response(status_code=status.HTTP_204_NO_CONTENT)


# #### Update a Post ####
# #######################
# #using existing post schema
# @app.put("/posts/{id}")
# def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
#     post_query = db.query(models.Post).filter(models.Post.uuid == id)
#     post = post_query.first()
#     if post == None:        
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Post with id: {id} doesn't exists.")
#     post_query.update(updated_post.dict(), synchronize_session=False)
#     db.commit()
#     return {"data": post_query.first()}

# # def update_post(id: int, post: Post):
# #     cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE uuid = %s RETURNING *""", (
# #         post.title, post.content, post.published, str(id),
# #     ))
# #     updated_post = cursor.fetchone()
# #     conn.commit()
#     # if updated_post == None:        
#     # index = find_index_post(id)
#     # if index == None:
#         # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#         #                     detail=f"Post with id: {id} doesn't exists.")
#     # post_dict = post.dict()
#     # post_dict['id'] = id
#     # my_post[index] = post_dict
#     # return {"data": updated_post}

# # # Extract all the fields from the request body
# # def create_posts(payload: dict = Body(...)):
# #     # title str, content str, category, boolean published
# #     print(payload)
# #     return {"message": "Post created successfully"}

# # @app.get("/hello/{name}")
# # async def say_hello(name: str):
# #     return {"message": f"Hello {name}"}
