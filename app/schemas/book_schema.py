from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class BookBase(BaseModel):
    title: str
    author: str 

class BookCreate(BookBase):
    user_id: int
    cover_img:str
    content_path:str
 
class BookRead(BookCreate):
    id: int 
    cover_img:str
    content_path:str
    model_config = ConfigDict(from_attributes=True)

class UploadBookResponse(BaseModel):
    file_name: str
    pages: int