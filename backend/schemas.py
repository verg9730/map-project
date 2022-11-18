from typing import List
import datetime
from pydantic import BaseModel

class Memo(BaseModel):

    user_id : int
    point_id : int
    memo_type : int
    memo_x : float
    memo_y : float
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

class Point(BaseModel):

    postal_code : str

    memos : List[Memo] = []
    class Config:
        orm_mode = True
        