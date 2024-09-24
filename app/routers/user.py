from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db_context
from schemas import User, CreateUser
from services import user as UserService

router = APIRouter(prefix="/users", tags=["Users"])

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=User)
def create_user(user: CreateUser, db: Session = Depends(get_db_context)):
    return UserService.create_user(user, db)

@router.get('/{id}', response_model=User)
def get_user(id: int, db: Session = Depends(get_db_context)):
    return UserService.get_user(id, db)