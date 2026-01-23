from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from app.db.session import Base
from app.db.base_class import TimestampMixin


class DocumentType(str, enum.Enum):
    """
    Enum for document types.
    
    Enum = a set of named values (like multiple choice options)
    This ensures only valid types can be stored.
    """
    ACADEMIC = "academic"      # Research papers, journal articles
    COURSE = "course"          # Lecture notes, assignments
    CODE = "code"              # Programming documentation
    OTHER = "other"            # Anything else


class Document(Base, TimestampMixin):
    """
    Document model.
    
    Attributes:
        id: Primary key
        title: Document title
        description: Optional description
        file_path: S3 path to the file
        file_type: Extension (.pdf, .docx, etc.)
        doc_type: Category (academic, course, code)
        size_bytes: File size in bytes
        chunk_count: Number of text chunks created
        owner_id: Foreign key to User
        
    Relationships:
        owner: The user who uploaded this document
    """
    
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Document metadata
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    file_path = Column(String, nullable=False)  # S3 path
    file_type = Column(String, nullable=False)  # .pdf, .docx, etc.
    doc_type = Column(Enum(DocumentType), default=DocumentType.OTHER)
    size_bytes = Column(Integer, nullable=False)
    
    # Processing status
    chunk_count = Column(Integer, default=0)  # Number of chunks created
    
    # Foreign key to User
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationship
    owner = relationship("User", back_populates="documents")
    
    def __repr__(self):
        return f"<Document {self.title}>"