from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class SoloSessionQuoteBase(BaseModel):
    solo_session_id: int    

class SoloSessionQuoteCreate(SoloSessionQuoteBase):
    selected_text:str
    color:str
    start_index:int
    end_index:int
 
class SoloSessionQuoteRead(SoloSessionQuoteCreate):
    id: int 
    model_config = ConfigDict(from_attributes=True)
