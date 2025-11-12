from datetime import datetime, timedelta
from typing import Optional, Union, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
import uuid

from .config import settings
from .database import get_session
from ..models.database import User

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token security
security = HTTPBearer()

# JWT Configuration
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """Create a JWT access token"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject), "type": "access"}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """Create a JWT refresh token"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[str]:
    """Verify and decode a JWT token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return user_id
    except JWTError:
        return None


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> User:
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        user_id = verify_token(credentials.credentials)
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Get user from database
    user = session.exec(select(User).where(User.id == user_id)).first()
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


def get_current_verified_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current verified user"""
    if not current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email not verified"
        )
    return current_user


def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    """Authenticate user with email and password"""
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_user_tokens(user: User) -> dict:
    """Create access and refresh tokens for user"""
    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


def refresh_user_token(refresh_token: str) -> Optional[dict]:
    """Refresh user access token using refresh token"""
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")
        
        if user_id is None or token_type != "refresh":
            return None
        
        # Create new access token
        access_token = create_access_token(subject=user_id)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
    except JWTError:
        return None


def check_user_permissions(user: User, required_role: str) -> bool:
    """Check if user has required role permissions"""
    role_hierarchy = {
        "free": 0,
        "starter": 1,
        "pro": 2,
        "enterprise": 3
    }
    
    user_level = role_hierarchy.get(user.role.value, 0)
    required_level = role_hierarchy.get(required_role, 0)
    
    return user_level >= required_level


def require_role(required_role: str):
    """Decorator to require specific user role"""
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if not check_user_permissions(current_user, required_role):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required role: {required_role}"
            )
        return current_user
    return role_checker


def check_video_limit(user: User) -> bool:
    """Check if user has reached their video generation limit"""
    from ..models.database import UserRole
    
    limits = {
        UserRole.FREE: 5,
        UserRole.STARTER: 20,
        UserRole.PRO: 100,
        UserRole.ENTERPRISE: float('inf')
    }
    
    limit = limits.get(user.role, 5)
    if limit == float('inf'):
        return True
    
    return user.videos_generated_this_month < limit


def increment_video_count(user: User, session: Session):
    """Increment user's video generation count"""
    user.videos_generated_this_month += 1
    user.videos_generated_total += 1
    session.add(user)
    session.commit()


def reset_monthly_usage(session: Session):
    """Reset monthly usage for all users (run monthly)"""
    users = session.exec(select(User)).all()
    for user in users:
        user.videos_generated_this_month = 0
        user.last_reset_date = datetime.utcnow()
        session.add(user)
    session.commit()


# Import Redis rate limiter
from .redis_rate_limiter import rate_limiter as redis_rate_limiter


def check_rate_limit(user_id: str, limit: int = 60, window: int = 60, method: str = "sliding"):
    """
    Check rate limit for user using distributed Redis rate limiter

    Args:
        user_id: User identifier
        limit: Maximum requests allowed
        window: Time window in seconds
        method: "fixed" or "sliding" window (default: sliding for better accuracy)

    Raises:
        HTTPException: If rate limit exceeded
    """
    if not redis_rate_limiter.is_allowed(user_id, limit, window, method):
        # Get status for helpful error message
        status_info = redis_rate_limiter.get_status(user_id, limit, window)

        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded",
            headers={
                "X-RateLimit-Limit": str(limit),
                "X-RateLimit-Remaining": str(status_info.get("remaining", 0)),
                "X-RateLimit-Reset": status_info.get("reset_at", ""),
                "Retry-After": str(window)
            }
        )