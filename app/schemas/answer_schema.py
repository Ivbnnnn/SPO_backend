from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class AnswerBase(BaseModel):
    participant_id: int
    note_id:int    

class AnswerCreate(AnswerBase):
    content: str
    session_id:int
 
class AnswerUpdate(AnswerBase):
    id:int
    content: str
    model_config = ConfigDict(from_attributes=True)
 
class AnswerDelete(AnswerBase):
    id:int 
    model_config = ConfigDict(from_attributes=True)
 
class AnswerRead(AnswerCreate):
    id: int 
    model_config = ConfigDict(from_attributes=True)
