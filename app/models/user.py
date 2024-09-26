from sqlalchemy import Column, String

from ..database import Base
from .base_entity import BaseEntity

class User(BaseEntity, Base):
    __tablename__ = "users"
    
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    
