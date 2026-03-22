from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class UserBase(BaseModel):
    user_name: str
    age: Optional[int] = None

class UserCreate(UserBase):
    user_password: str

class UserUpdate(UserCreate):
    user_name: Optional[str] = None
    age: Optional[int] = None
    user_password: Optional[str] = None

class UserRead(UserBase):
    user_id: int
    model_config = ConfigDict(from_attributes=True)
