from fastapi import APIRouter, Depends, status
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db_context, get_async_db_context
from schemas import Post, CreatePost, UpdatePost
from models import User as UserModel
from services import post as PostService, auth as AuthService

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/", response_model=list[Post])
async def get_all_posts(async_db: AsyncSession = Depends(get_async_db_context),
                        current_user: UserModel = Depends(AuthService.get_current_user),
                        limit: int = 10, offset: int = 0, search: Optional[str] = ""):
    user_id = current_user.id
    return await PostService.get_all_posts(async_db, user_id, limit, offset, search)

@router.get("/{id}", response_model=Post)
def get_post(id: int, db: Session = Depends(get_db_context), current_user: UserModel = Depends(AuthService.get_current_user)):
    user_id = current_user.id
    return PostService.get_post(id, db, user_id)
    
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
async def create_post(post: CreatePost, db: Session = Depends(get_db_context), current_user: UserModel = Depends(AuthService.get_current_user)):
    user_id = current_user.id
    return PostService.create_post(post, db, user_id)

@router.put("/{id}", response_model=Post)
def update_post(id: int, updated_post: UpdatePost, db: Session = Depends(get_db_context), current_user: UserModel = Depends(AuthService.get_current_user)):
    user_id = current_user.id
    return PostService.update_post(id, updated_post, db, user_id)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db_context), current_user: UserModel = Depends(AuthService.get_current_user)):
    user_id = current_user.id
    return PostService.delete_post(id, db, user_id)