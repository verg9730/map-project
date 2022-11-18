from database import Base
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(32))
    user_email = Column(String(32))
    memos = relationship("Memo", back_populates="writer")      

class Point(Base):
    
    __tablename__ = 'point'

    id = Column(Integer, primary_key=True, index=True)
    postal_code = Column(String(32))
    memos = relationship("Memo", back_populates="postbox")

class Memo(Base):
    
    __tablename__ = 'memo'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    point_id = Column(Integer, ForeignKey("point.id"))
    memo_type = Column(Integer) #0:public 1:private
    memo_x = Column(Float(32))
    memo_y = Column(Float(32))
    memo_content = Column(String(32))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    writer = relationship("User", back_populates="memos")
    postbox = relationship("Point", back_populates="memos")