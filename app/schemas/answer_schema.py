from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class AnswerBase(BaseModel):
    content: str

class AnswerCreate(AnswerBase):
    participant_id: int
    note_id:int    
 
class AnswerRead(AnswerCreate):
    id: int 
    model_config = ConfigDict(from_attributes=True)
