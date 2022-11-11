from sqlalchemy import Boolean, Column, Integer, String
from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from typing import List
import datetime

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(32))
    user_email = Column(String(32))
    # created_at = Column(DateTime, default=datetime.datetime.utcnow)       

class Point(Base):
    
    __tablename__ = 'point'

    id = Column(Integer, primary_key=True, index=True)
    point_coordinate = List[Integer]
    point_range = Column(Integer)
    # created_at = Column(DateTime, default=datetime.datetime.utcnow)     

class Memo(Base):
    
    __tablename__ = 'memo'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    point_id = Column(Integer)
    memo_type = Column(String(32))
    point_coordinate = Column(Integer)
    memo_content = Column(String(32))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)       