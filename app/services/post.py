from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import Post as PostModel
from schemas import Post, CreatePost, UpdatePost

def get_all_posts(db: Session) -> list[Post]:
    return db.query(Post).all()

def get_post(id: int, db: Session) -> Post:
    post = db.query(PostModel).filter(PostModel.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
    
    return post

def create_post(post: CreatePost, db: Session) -> Post:
    print("[Service] Creating post...")
    print(post)
    new_post = PostModel(**post.dict()) # ** means unpacking the dictionary, same as spreading in JavaScript
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

def update_post(id: int, updated_post: UpdatePost, db: Session) -> Post:
    post = db.query(PostModel).filter(PostModel.id == id)
    
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    
    post.update(updated_post.dict(), synchronize_session=False)
    
    db.commit()
    
    return post.first()

def delete_post(id: int, db: Session) -> None:
    post = db.query(PostModel).filter(PostModel.id == id)
    
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    
    post.delete(synchronize_session=False)
    
    db.commit()