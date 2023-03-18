# Schema for what we want to gather for each FOI request we are indexing
from dataclasses import dataclass, field, asdict
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

    def asdict(self):
        d = asdict(self)
        if self.last_updated_at:
            d["last_updated_at"] = self.last_updated_at.isoformat()
        if self.initial_request_at:
            d["initial_request_at"] = self.initial_request_at.isoformat()
        return d
