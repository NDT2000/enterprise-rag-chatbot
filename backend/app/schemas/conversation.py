from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ConversationCreate(BaseModel):
    title: Optional[str] = "New Conversation"


class ConversationResponse(ConversationCreate):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True