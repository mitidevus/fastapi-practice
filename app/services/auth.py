from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional
from datetime import timedelta
from jose import jwt, JWTError

from . import utils
from ..models import User as UserModel
from ..schemas import TokenData
from ..settings import JWT_SECRET, JWT_ALGORITHM
from ..database import get_db_context

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_access_token(user: UserModel, expires: Optional[timedelta] = None):
    claims = {
        "sub": str(user.id),
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

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        id: str = payload.get("sub")

        if id is None:
            raise credentials_exception
        
        token_data = TokenData(id=id)
        return token_data
    except JWTError:
        raise credentials_exception
    
def get_current_user(token: str = Depends(oauth2_bearer), db: Session = Depends(get_db_context)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    token = verify_access_token(token, credentials_exception)
    
    user = db.query(UserModel).filter(UserModel.id == token.id).first()
    
    return user