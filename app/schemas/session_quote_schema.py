from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class SessionQuoteBase(BaseModel):
    session_id: int
    participant_id: int 

class SessionQuoteCreate(SessionQuoteBase):
    selected_text:str
    color:str
    start_index:int
    end_index:int
 
class SessionQuoteRead(SessionQuoteCreate):
    id: int 
    model_config = ConfigDict(from_attributes=True)
 