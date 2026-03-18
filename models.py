from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class Problem(Base):
    __tablename__ = "problems"
    
    id = Column(Integer, primary_key=True, index=True) 
    title = Column(String)
    platform = Column(String)
    difficulty = Column(String)
    topics = Column(String)
    notes = Column(String)
    created_at = Column(DateTime, default=datetime.now())

