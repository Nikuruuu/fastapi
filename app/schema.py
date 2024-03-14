from pydantic import BaseModel, EmailStr, UUID4
from datetime import datetime
from uuid import UUID


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: UUID
    created_at: datetime
    user_id: UUID  # ForeignKey to users.User

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    id: UUID
    title: str
    content: str
    published: bool
    created_at: datetime
    user_id: UUID

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: UUID
