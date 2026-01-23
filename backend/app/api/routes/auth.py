from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, Token, UserLogin
from app.core.security import hash_password, verify_password, create_access_token
from app.api.dependencies import get_current_user

# Create router
# prefix="/auth" means all routes start with /auth
# tags=["authentication"] groups these in API docs
router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user.
    
    **Process:**
    1. Check if email already exists
    2. Hash the password
    3. Create user in database
    4. Return user data (without password!)
    
    **Request Body:**
```json
    {
        "email": "user@example.com",
        "password": "securepassword123",
        "full_name": "John Doe"
    }
```
    
    **Response:**
```json
    {
        "id": 1,
        "email": "user@example.com",
        "full_name": "John Doe",
        "is_active": true,
        "is_superuser": false,
        "created_at": "2026-01-23T10:30:00"
    }
```
    
    **Errors:**
    - 400: Email already registered
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    db_user = User(
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        full_name=user_in.full_name,
        is_active=True,
        is_superuser=False
    )
    
    # Add to database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # Refresh to get the ID and timestamps
    
    return db_user


@router.post("/login", response_model=Token)
def login(
    user_credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login and get access token.
    
    **Process:**
    1. Find user by email
    2. Verify password
    3. Generate JWT token
    4. Return token
    
    **Request Body:**
```json
    {
        "email": "user@example.com",
        "password": "securepassword123"
    }
```
    
    **Response:**
```json
    {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "token_type": "bearer"
    }
```
    
    **Usage:**
    After receiving the token, include it in subsequent requests:
```
    Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```
    
    **Errors:**
    - 401: Invalid credentials
    - 400: Inactive user
    """
    # Find user by email
    user = db.query(User).filter(User.email == user_credentials.email).first()
    
    # Check if user exists and password is correct
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login/form", response_model=Token)
def login_form(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login using OAuth2 form (for Swagger UI "Authorize" button).
    
    This endpoint uses form data instead of JSON.
    It's required for the FastAPI docs "Authorize" feature to work.
    
    **Form Data:**
    - username: User's email (yes, it's called username in OAuth2 spec)
    - password: User's password
    
    **Response:** Same as /login endpoint
    """
    # Find user by email (form_data.username contains the email)
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    access_token = create_access_token(data={"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Get current user profile.
    
    **This is a protected endpoint** - requires authentication.
    
    **Headers Required:**
```
    Authorization: Bearer <your_access_token>
```
    
    **Response:**
```json
    {
        "id": 1,
        "email": "user@example.com",
        "full_name": "John Doe",
        "is_active": true,
        "is_superuser": false,
        "created_at": "2026-01-23T10:30:00"
    }
```
    
    **Errors:**
    - 401: Missing or invalid token
    - 400: Inactive user
    """
    return current_user