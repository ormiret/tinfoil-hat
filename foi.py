# Schema for what we want to gather for each FOI request we are indexing
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class FOI:
    title: str = ""
    last_updated_at: Optional[datetime] = None
    initial_request_at: Optional[datetime] = None
    link: str = "" # link to more details 
    status: str = "" # awaiting response, responded, information not held, FOI exception etc.
    tags: List[str] = field(default_factory=list)
    wdtk_id: str  = "" # What Do They Know ID
    body_id: str = "" # ID from the body FOI is sent to  
