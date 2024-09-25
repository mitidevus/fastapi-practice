from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from services import utils
from models import Post as PostModel, Vote as VoteModel
from schemas import Post, CreatePost, UpdatePost, PostOut

def get_all_posts(db: Session, limit: int, offset: int, search: str) -> list[PostOut]:
    posts = db.query(PostModel, func.count(VoteModel.post_id).label("votes")).join(
        VoteModel, VoteModel.post_id == PostModel.id, isouter=True).group_by(PostModel.id).filter(PostModel.title.contains(search)).limit(limit).offset(offset).all()
    
    return posts
    

def get_post(id: int, db: Session) -> PostOut:
    post = db.query(PostModel, func.count(VoteModel.post_id).label("votes")).join(
        VoteModel, VoteModel.post_id == PostModel.id, isouter=True).group_by(PostModel.id).filter(PostModel.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
    
    return post

def create_post(post: CreatePost, db: Session, user_id: str) -> Post:
    new_post = PostModel(owner_id=user_id, **post.model_dump()) # ** means unpacking the dictionary, same as spreading in JavaScript
    
    new_post.created_at = utils.get_current_utc_time()
    new_post.updated_at = utils.get_current_utc_time()
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

def update_post(id: int, updated_post: UpdatePost, db: Session, user_id: str) -> Post:
    post_query = db.query(PostModel).filter(PostModel.id == id)
    
    post = post_query.first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    
    if post.owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    
    db.commit()
    
    return post.first()

def delete_post(id: int, db: Session, user_id: str) -> None:
    post_query = db.query(PostModel).filter(PostModel.id == id)
    
    post = post_query.first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    
    if post.owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    
    db.commit()