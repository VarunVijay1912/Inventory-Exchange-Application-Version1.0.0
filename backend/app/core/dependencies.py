"""Enhanced dependency injection"""
from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.core.security import verify_token
from app.core.logging import logger
from app.core.exceptions import UnauthorizedError, ForbiddenError

security = HTTPBearer()


def get_db() -> Generator:
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """Get current authenticated user"""
    
    token = credentials.credentials
    user_id = verify_token(token, "access")
    
    if user_id is None:
        logger.warning("Invalid or expired token")
        raise UnauthorizedError("Could not validate credentials")
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if user is None:
        logger.warning(f"User not found for ID: {user_id}")
        raise UnauthorizedError("User not found")
    
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current active user"""
    if not current_user.is_active:
        logger.warning(f"Inactive user attempted access: {current_user.id}")
        raise ForbiddenError("Inactive user account")
    
    return current_user


def get_current_verified_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """Get current verified user"""
    if not current_user.is_verified:
        logger.warning(f"Unverified user attempted restricted access: {current_user.id}")
        raise ForbiddenError("User account not verified")
    
    return current_user


def get_optional_user(
    db: Session = Depends(get_db),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[User]:
    """Get current user if authenticated, None otherwise"""
    if credentials is None:
        return None
    
    try:
        token = credentials.credentials
        user_id = verify_token(token, "access")
        
        if user_id is None:
            return None
        
        user = db.query(User).filter(User.id == user_id).first()
        return user
        
    except Exception:
        return None