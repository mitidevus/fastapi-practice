from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from services import utils
from models import User as UserModel
from schemas import User, CreateUser

def create_user(user: CreateUser, db: Session) -> User:
    new_user = UserModel(**user.model_dump()) # ** means unpacking the dictionary, same as spreading in JavaScript
    
    new_user.password = utils.hash(user.password)
    new_user.created_at = utils.get_current_utc_time()
    new_user.updated_at = utils.get_current_utc_time()
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

def get_user(id: int, db: Session) -> User:
    user = db.query(UserModel).filter(UserModel.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} does not exist")
    
    return user