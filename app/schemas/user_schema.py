from pydantic import BaseModel, ConfigDict, EmailStr
from typing import List, Optional


class UserBase(BaseModel):
    name: str
    last_name: Optional[str] = None

class UserCreate(UserBase):
    password: str 
    email: EmailStr 
    background_color:Optional[str] = None
    font_size:Optional[str] = None

class UserUpdate(UserCreate):
    model_config = ConfigDict(from_attributes=True)

class UserRead(UserBase):
    id: int
    background_color:str
    font_size:str
    model_config = ConfigDict(from_attributes=True)
