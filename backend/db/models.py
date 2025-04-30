# backend/db/models.py

from sqlalchemy import Column, Integer, String
from backend.db.session import Base

class GuessCounter(Base):
    __tablename__ = 'guess_counter'
    
    id = Column(Integer, primary_key=True, index=True)
    count = Column(Integer, default=0)
