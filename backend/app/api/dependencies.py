from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import decode_access_token
from app.models.user import User

# HTTPBearer scheme - simpler than OAuth2PasswordBearer
# This creates a simple "Bearer Token" input in Swagger UI
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get the current authenticated user.
    
    Extracts and validates JWT token from Authorization header.
    
    Usage in endpoints:
        @app.get("/profile")
        def get_profile(current_user: User = Depends(get_current_user)):
            return current_user
    
    Args:
        credentials: HTTP credentials with bearer token
        db: Database session
        
    Returns:
        User object if token is valid
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    # Define exception for invalid credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Extract token from credentials
    token = credentials.credentials
    
    # Decode token to get email
    email = decode_access_token(token)
    
    if email is None:
        raise credentials_exception
    
    # Fetch user from database
    user = db.query(User).filter(User.email == email).first()
    
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    return user


def get_current_active_superuser(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to require superuser privileges.
    
    Use this for admin-only endpoints.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough privileges"
        )
    
    return current_user