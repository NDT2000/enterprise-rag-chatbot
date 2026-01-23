from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.base_class import TimestampMixin


class User(Base, TimestampMixin):
    """
    User model.
    
    Attributes:
        id: Primary key
        email: Unique user email (used for login)
        hashed_password: Bcrypt hash of user's password
        full_name: User's display name
        is_active: Whether the account is active (for soft deletion)
        is_superuser: Admin privileges
        
    Relationships:
        documents: All documents uploaded by this user
        conversations: All conversations started by this user
    """
    
    __tablename__ = "users"
    
    # Primary key - auto-incrementing integer
    id = Column(Integer, primary_key=True, index=True)
    
    # Email - unique constraint ensures no duplicate emails
    email = Column(String, unique=True, index=True, nullable=False)
    
    # Password hash - NEVER store plain text passwords
    hashed_password = Column(String, nullable=False)
    
    # User information
    full_name = Column(String, nullable=True)
    
    # Status flags
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    # Relationships (foreign keys defined in other models)
    # These allow: user.documents, user.conversations
    documents = relationship("Document", back_populates="owner")
    conversations = relationship("Conversation", back_populates="user")
    
    def __repr__(self):
        """String representation for debugging."""
        return f"<User {self.email}>"