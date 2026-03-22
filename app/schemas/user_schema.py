from pydantic import BaseModel, ConfigDict, EmailStr
from typing import List, Optional


class UserBase(BaseModel):
    name: str
    last_name: Optional[str] = None

class UserCreate(UserBase):
    password: Optional[str] = None
    email: Optional[EmailStr] = None

class UserUpdate(UserCreate):
    model_config = ConfigDict(from_attributes=True)

class UserRead(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
