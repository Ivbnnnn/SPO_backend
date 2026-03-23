from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class SessionAnswerBase(BaseModel):
    note_id: int
    participant_id: int 

class SessionAnswerCreate(SessionAnswerBase):
    content:str
 
class SessionAnswerRead(SessionAnswerCreate):
    id: int 
    model_config = ConfigDict(from_attributes=True)
