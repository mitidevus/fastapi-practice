from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from datetime import timedelta
from jose import jwt

from services import utils
from schemas import LoginPayload
from models import User as UserModel
from settings import JWT_SECRET, JWT_ALGORITHM

def create_access_token(user: UserModel, expires: Optional[timedelta] = None):
    claims = {
        "sub": user.id,
        "email": user.email,
    }
    expire = utils.get_current_utc_time() + expires if expires else utils.get_current_utc_time() + timedelta(minutes=10)
    claims.update({"exp": expire})
    return jwt.encode(claims, JWT_SECRET, algorithm=JWT_ALGORITHM)
 
    

def login (email: str, password: str, db: Session):
    user = db.query(UserModel).filter(UserModel.email == email).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid email or password")
    
    if not utils.verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid email or password")
    
    return {"access_token": create_access_token(user, timedelta(minutes=10)), "token_type": "bearer"}