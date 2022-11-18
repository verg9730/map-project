from ssl import create_default_context
from typing import Union, List
import datetime
from pydantic import BaseModel

class Memo(BaseModel):

    user_id : int
    point_id : int
    memo_type : str
    memo_x : int
    memo_y : int
    memo_content : str
    created_at : datetime.datetime    
    class Config:
        orm_mode = True
        
class User(BaseModel):

    user_name : str
    user_email : str

    memos : List[Memo] = []
    class Config:
        orm_mode = True
    # created_at = Column(DateTime, default=datetime.datetime.utcnow)       

class Point(BaseModel):

    point_x : int
    point_y : int
    point_range : int

    memos : List[Memo] = []
    # created_at = Column(DateTime, default=datetime.datetime.utcnow)     
    class Config:
        orm_mode = True
        
