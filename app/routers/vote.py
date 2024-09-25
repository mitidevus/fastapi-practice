from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db_context
from schemas import VotePayload
from models import User as UserModel
from services import vote as VoteService, auth as AuthService


router = APIRouter(prefix="/votes", tags=["Votes"])

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_vote(vote_payload: VotePayload, db: Session = Depends(get_db_context), current_user: UserModel = Depends(AuthService.get_current_user)):
    user_id = current_user.id
    return VoteService.create_vote(vote_payload, db, user_id)

@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
def delete_vote(vote_payload: VotePayload, db: Session = Depends(get_db_context), current_user: UserModel = Depends(AuthService.get_current_user)):
    user_id = current_user.id
    return VoteService.delete_vote(vote_payload, db, user_id)