from pydantic import BaseModel
from datetime import datetime

from .user import User

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
class CreatePost(PostBase):
    pass # No additional fields needed

class UpdatePost(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    owner_id: int
    owner: User
    
    class Config:
        orm_mode = True
        
class PostOut(BaseModel):
    Post: Post
    votes: int
    
    class Config:
        orm_mode = True