from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class MessageCreate(BaseModel):
    content: str
    conversation_id: int


class MessageResponse(MessageCreate):
    id: int
    is_user: bool
    sources: Optional[List[Dict[str, Any]]] = None
    token_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True