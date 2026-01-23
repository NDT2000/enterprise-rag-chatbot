from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.document import DocumentType


class DocumentCreate(BaseModel):
    title: str
    description: Optional[str] = None
    file_path: str
    file_type: str
    doc_type: DocumentType
    size_bytes: int


class DocumentResponse(DocumentCreate):
    id: int
    owner_id: int
    chunk_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True