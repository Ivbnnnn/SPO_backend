from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class SoloSessionNoteBase(BaseModel):
    solo_session_id: int    

class SoloSessionNoteCreate(SoloSessionNoteBase):
    selected_text:str
    color:str
    comment:str
    start_index:int
    end_index:int

class SoloSessionNoteUpdate(SoloSessionNoteBase):
    id:int
    selected_text:str
    color:str
    comment:str
    start_index:int
    end_index:int
 
class SoloSessionNoteRead(SoloSessionNoteCreate):
    id: int 
    model_config = ConfigDict(from_attributes=True)

class SoloSessionNoteDelete(SoloSessionNoteBase):
    id: int 
    model_config = ConfigDict(from_attributes=True)
