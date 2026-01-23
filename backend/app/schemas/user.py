from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema with common fields."""
    email: EmailStr  # Validates email format
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """
    Schema for user registration.
    
    What user sends when registering:
    POST /auth/register
    {
        "email": "user@example.com",
        "password": "securepassword123",
        "full_name": "John Doe"
    }
    """
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")


class UserLogin(BaseModel):
    """
    Schema for user login.
    
    What user sends when logging in:
    POST /auth/login
    {
        "email": "user@example.com",
        "password": "securepassword123"
    }
    """
    email: EmailStr
    password: str


class UserResponse(UserBase):
    """
    Schema for user data in responses.
    
    What API returns after successful registration or when fetching user profile.
    Note: We NEVER return the password!
    """
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    
    class Config:
        """
        Pydantic configuration.
        
        orm_mode = True allows Pydantic to read data from SQLAlchemy models.
        This means we can do: UserResponse.from_orm(user_db_object)
        """
        from_attributes = True  # Pydantic v2 (was orm_mode in v1)


class Token(BaseModel):
    """
    Schema for JWT token response.
    
    What API returns after successful login:
    {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "token_type": "bearer"
    }
    
    User then sends this token in Authorization header:
    Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
    """
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """
    Schema for data extracted from JWT token.
    
    After decoding the token, we get the user's email.
    """
    email: Optional[str] = None