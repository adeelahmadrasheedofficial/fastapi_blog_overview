from pydantic import BaseModel, EmailStr, BaseSettings
from datetime import datetime
from typing import Optional

from pydantic.types import conint


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


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


# Pydantic model for returned data
class PostResponse(PostBase):
    uuid: int
    user_uuid: int
    created_at: datetime
    creator: UserResponse

    class Config:
        orm_mode = True


class VoteCreate(BaseModel):
    post_uuid: int
    dir: conint(le=1)


class PostOut(PostBase):
    votes: int
