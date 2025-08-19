from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlmodel import Session, select
from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid

from ..core.database import get_session
from ..core.security import (
    get_password_hash, 
    verify_password, 
    create_user_tokens, 
    get_current_user,
    refresh_user_token,
    authenticate_user
)
from ..models.database import User, UserRole

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Pydantic models for request/response
class UserSignup(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    company: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenRefresh(BaseModel):
    refresh_token: str

class UserResponse(BaseModel):
    id: str
    email: str
    full_name: Optional[str] = None
    company: Optional[str] = None
    role: UserRole
    is_verified: bool
    videos_generated_this_month: int
    videos_generated_total: int

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    user: UserResponse


@router.post("/signup", response_model=TokenResponse)
async def signup(user_data: UserSignup, session: Session = Depends(get_session)):
    """Register a new user"""
    
    # Check if user already exists
    existing_user = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Validate password strength
    if len(user_data.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        company=user_data.company,
        role=UserRole.FREE
    )
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    # Generate tokens
    tokens = create_user_tokens(new_user)
    
    # Return user data and tokens
    return TokenResponse(
        **tokens,
        user=UserResponse(
            id=new_user.id,
            email=new_user.email,
            full_name=new_user.full_name,
            company=new_user.company,
            role=new_user.role,
            is_verified=new_user.is_verified,
            videos_generated_this_month=new_user.videos_generated_this_month,
            videos_generated_total=new_user.videos_generated_total
        )
    )


@router.post("/login", response_model=TokenResponse)
async def login(user_data: UserLogin, session: Session = Depends(get_session)):
    """Authenticate user and return tokens"""
    
    # Authenticate user
    user = authenticate_user(session, user_data.email, user_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account is deactivated"
        )
    
    # Generate tokens
    tokens = create_user_tokens(user)
    
    # Return user data and tokens
    return TokenResponse(
        **tokens,
        user=UserResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            company=user.company,
            role=user.role,
            is_verified=user.is_verified,
            videos_generated_this_month=user.videos_generated_this_month,
            videos_generated_total=user.videos_generated_total
        )
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(token_data: TokenRefresh, session: Session = Depends(get_session)):
    """Refresh access token using refresh token"""
    
    # Refresh token
    new_tokens = refresh_user_token(token_data.refresh_token)
    
    if not new_tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Get user from refresh token
    from ..core.security import verify_token
    user_id = verify_token(token_data.refresh_token)
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user = session.exec(select(User).where(User.id == user_id)).first()
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Return new tokens and user data
    return TokenResponse(
        **new_tokens,
        user=UserResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            company=user.company,
            role=user.role,
            is_verified=user.is_verified,
            videos_generated_this_month=user.videos_generated_this_month,
            videos_generated_total=user.videos_generated_total
        )
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        company=current_user.company,
        role=current_user.role,
        is_verified=current_user.is_verified,
        videos_generated_this_month=current_user.videos_generated_this_month,
        videos_generated_total=current_user.videos_generated_total
    )


@router.post("/logout")
async def logout():
    """Logout user (client should discard tokens)"""
    # In a stateless JWT system, logout is handled client-side
    # by discarding the tokens
    return {"message": "Successfully logged out"}


@router.post("/verify-email")
async def verify_email(token: str, session: Session = Depends(get_session)):
    """Verify user email address"""
    # This would implement email verification logic
    # For now, return a placeholder response
    return {"message": "Email verification endpoint - implement verification logic"}


@router.post("/forgot-password")
async def forgot_password(email: EmailStr, session: Session = Depends(get_session)):
    """Send password reset email"""
    # Check if user exists
    user = session.exec(select(User).where(User.email == email)).first()
    
    if not user:
        # Don't reveal if email exists or not
        return {"message": "If the email exists, a password reset link has been sent"}
    
    # This would implement password reset email logic
    # For now, return a placeholder response
    return {"message": "Password reset email sent (if email exists)"}


@router.post("/reset-password")
async def reset_password(token: str, new_password: str, session: Session = Depends(get_session)):
    """Reset password using reset token"""
    # This would implement password reset logic
    # For now, return a placeholder response
    return {"message": "Password reset endpoint - implement reset logic"}


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    full_name: Optional[str] = None,
    company: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update user profile"""
    
    if full_name is not None:
        current_user.full_name = full_name
    
    if company is not None:
        current_user.company = company
    
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        company=current_user.company,
        role=current_user.role,
        is_verified=current_user.is_verified,
        videos_generated_this_month=current_user.videos_generated_this_month,
        videos_generated_total=current_user.videos_generated_total
    )


@router.delete("/account")
async def delete_account(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete user account"""
    # This would implement account deletion logic
    # For now, just deactivate the account
    current_user.is_active = False
    session.add(current_user)
    session.commit()
    
    return {"message": "Account deactivated successfully"}