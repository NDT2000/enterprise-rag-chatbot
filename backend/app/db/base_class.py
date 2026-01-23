from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declared_attr


class TimestampMixin:
    """
    Mixin that adds created_at and updated_at timestamps to models.
    
    Mixin = a class that provides functionality to other classes
    Every model that uses this will automatically get these two columns.
    """
    
    created_at = Column(
        DateTime,
        default=datetime.utcnow,  # Automatically set when row is created
        nullable=False
    )
    
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,  # Automatically update when row changes
        nullable=False
    )