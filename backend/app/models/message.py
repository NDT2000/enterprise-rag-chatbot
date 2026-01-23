from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.base_class import TimestampMixin


class Message(Base, TimestampMixin):
    """
    Message model.
    
    Stores individual messages in conversations.
    Both user messages and AI responses are stored here.
    
    Attributes:
        id: Primary key
        content: The actual message text
        is_user: True if message from user, False if from AI
        conversation_id: Foreign key to Conversation
        sources: JSON array of document sources used (for AI responses)
        token_count: Number of tokens used (for cost tracking)
        
    Relationships:
        conversation: The conversation this message belongs to
    """
    
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    is_user = Column(Boolean, nullable=False)  # True = user, False = AI
    
    # Foreign key to Conversation
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    
    # Additional metadata
    sources = Column(JSON, nullable=True)  # List of document IDs used for response
    token_count = Column(Integer, default=0)  # For cost tracking
    
    # Relationship
    conversation = relationship("Conversation", back_populates="messages")
    
    def __repr__(self):
        role = "User" if self.is_user else "AI"
        preview = self.content[:50] + "..." if len(self.content) > 50 else self.content
        return f"<Message {role}: {preview}>"