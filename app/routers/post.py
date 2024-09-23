from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db_context
from schemas import Post, CreatePost, UpdatePost
from services import post as PostService

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/", response_model=list[Post])
def get_all_posts(db: Session = Depends(get_db_context)):
    return PostService.get_all_posts(db)

@router.get("/{id}", response_model=Post)
def get_post(id: int, db: Session = Depends(get_db_context)):
    return PostService.get_post(id, db)
    
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(post: CreatePost, db: Session = Depends(get_db_context)):
    print("[Router] Creating post...")
    print(post)
    return PostService.create_post(post, db)

@router.put("/{id}", response_model=Post)
def update_post(id: int, updated_post: UpdatePost, db: Session = Depends(get_db_context)):
    return PostService.update_post(id, updated_post, db)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db_context)):
    return PostService.delete_post(id, db)