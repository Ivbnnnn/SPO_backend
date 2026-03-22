from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class ItemBase(BaseModel):
    item_name: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    owner_id: int

class ItemRead(ItemCreate):
    item_id: int
    owner_id: int
    src:str
    model_config = ConfigDict(from_attributes=True)

