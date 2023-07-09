from pydantic import BaseModel
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