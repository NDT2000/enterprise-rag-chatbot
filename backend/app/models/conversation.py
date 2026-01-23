from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.base_class import TimestampMixin


class Conversation(Base, TimestampMixin):
    """
    Conversation model.
    
    A conversation contains multiple messages between user and AI.
    Think of it like a WhatsApp chat thread.
    
    Attributes:
        id: Primary key
        title: Conversation title (auto-generated from first message)
        user_id: Foreign key to User
        
    Relationships:
        user: The user who started this conversation
        messages: All messages in this conversation
    """
    
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, default="New Conversation")
    
    # Foreign key to User
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    # cascade="all, delete-orphan" means: if conversation is deleted, delete all messages too
    
    def __repr__(self):
        return f"<Conversation {self.title}>"