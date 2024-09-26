from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..schemas import VotePayload
from ..models import Vote as VoteModel, Post as PostModel

def create_vote(vote_payload: VotePayload, db: Session, user_id: str):
    post = db.query(PostModel).filter(PostModel.id == vote_payload.post_id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {vote_payload.post_id} does not exist")
    
    vote_query = db.query(VoteModel).filter(VoteModel.post_id == vote_payload.post_id, VoteModel.user_id == user_id)
    
    if vote_query.first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {user_id} has already voted for post {vote_payload.post_id}")
    
    new_vote = VoteModel(post_id=vote_payload.post_id, user_id=user_id)
    db.add(new_vote)
    db.commit()
    return {"message": "Created vote successfully"}

def delete_vote(vote_payload: VotePayload, db: Session, user_id: str):
    vote_query = db.query(VoteModel).filter(VoteModel.post_id == vote_payload.post_id, VoteModel.user_id == user_id)
    
    if not vote_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} has not voted for post {vote_payload.post_id}")
    
    vote_query.delete(synchronize_session=False) 
    db.commit()
    return None
    