from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class SessionNoteBase(BaseModel):
    session_id: int
    participant_id: int 

class SessionNoteCreate(SessionNoteBase):
    selected_text:str
    color:str
    is_private:bool
    comment:str
    start_index:int
    end_index:int
 
class SessionNoteRead(SessionNoteCreate):
    id: int 
    model_config = ConfigDict(from_attributes=True)
