from pydantic import BaseModel, EmailStr
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass

# Pydantic model for returned data
class PostResponse(PostBase):
    uuid: int
    created_at: datetime
    
    class Config:
        orm_mode = True
        
        
## Creating user schema
class UserCreate(BaseModel):
    # uuid: int
    email: EmailStr
    password: str

    

class UserResponse(BaseModel):
    uuid: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True