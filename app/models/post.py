from sqlalchemy import Boolean, Column, String
from database import Base
from .base_entity import BaseEntity

class Post(BaseEntity, Base):
    __tablename__ = "posts"
    
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE')