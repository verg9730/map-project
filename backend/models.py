from sqlalchemy import Boolean, Column, Integer, String
from database import Base

class Chicken(Base):
    __tablename__ = "topic"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    created = Column(String)
    author = Column(String)
    profile = Column(String, default=False)
