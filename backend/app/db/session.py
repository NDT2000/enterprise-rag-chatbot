from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create database engine
# echo=True means print all SQL queries (useful for debugging)
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG, # Only log SQL in development
    pool_pre_ping=True # Verify connections before using
)

# SessionLocal = factory for creating database sessions
# autocommit=False: We control when to save
# autoflush=False: We control when to send changes to DB
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all database models
# All our models (User, Document, etc.) will inherit from this
Base = declarative_base()

def get_db():
    """
    Dependency function that provides a database session.
    
    This is used by FastAPI to inject database sessions into endpoints.
    The session is automatically closed after the request completes.
    
    Yields:
        Session: Database session
        
    Example usage in an endpoint:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            users = db.query(User).all()
            return users
    """
    db = SessionLocal()
    try:
        yield db # Give the session to the endpoint
    finally:
        db.close() # Always close the session, even if there is an error