from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings

# Password hashing context
# bcrypt is slow by design - makes brute force attacks harder
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password string
        
    Example:
        >>> hash_password("mypassword123")
        '$2b$12$KIXxkjhsd...'
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against its hash.
    
    Args:
        plain_password: Password entered by user
        hashed_password: Hash stored in database
        
    Returns:
        True if password matches, False otherwise
        
    Example:
        >>> hashed = hash_password("mypassword123")
        >>> verify_password("mypassword123", hashed)
        True
        >>> verify_password("wrongpassword", hashed)
        False
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    JWT Structure:
    - Header: Algorithm info (HS256)
    - Payload: User data (email, user_id, expiration)
    - Signature: Cryptographic signature to verify authenticity
    
    Args:
        data: Dictionary containing user information (usually {"sub": user_email})
        expires_delta: Optional custom expiration time
        
    Returns:
        Encoded JWT token string
        
    Example:
        >>> token = create_access_token({"sub": "user@example.com"})
        >>> print(token)
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
    """
    to_encode = data.copy()
    
    # Set expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Add expiration to token payload
    to_encode.update({"exp": expire})
    
    # Encode and sign the token
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt


def decode_access_token(token: str) -> Optional[str]:
    """
    Decode and validate a JWT token.
    
    Args:
        token: JWT token string
        
    Returns:
        Email (subject) from token if valid, None if invalid
        
    Example:
        >>> token = create_access_token({"sub": "user@example.com"})
        >>> decode_access_token(token)
        'user@example.com'
    """
    try:
        # Decode the token
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        
        # Extract email (subject)
        email: str = payload.get("sub")
        
        if email is None:
            return None
            
        return email
        
    except JWTError:
        # Token is invalid, expired, or tampered with
        return None