"""Enhanced authentication endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.core.security import create_access_token, create_refresh_token, verify_token
from app.schemas.auth import LoginRequest, Token, RefreshTokenRequest
from app.schemas.user import UserCreate, User
from app.services.auth_service import AuthService
from app.utils.validators import verify_gst_number_api
from app.config import settings
from app.core.logging import logger
from app.core.exceptions import UnauthorizedError, ConflictError, ValidationError

router = APIRouter()


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(user_create: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user
    
    - Validates unique email, phone, and GST
    - Creates user account (unverified by default)
    - Returns user profile
    """
    try:
        # Check if user already exists
        if AuthService.get_user_by_email(db, user_create.email):
            raise ConflictError("Email already registered")
        
        if AuthService.get_user_by_gst(db, user_create.gst_number):
            raise ConflictError("GST number already registered")
        
        if AuthService.get_user_by_phone(db, user_create.phone):
            raise ConflictError("Phone number already registered")
        
        # Create user
        logger.info(f"Creating new user: {user_create.email}")
        user = AuthService.create_user(db, user_create)
        logger.info(f"User created successfully: {user.id}")
        
        return user
        
    except ConflictError:
        raise
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed. Please try again."
        )


@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    User login
    
    - Authenticates user credentials
    - Returns access and refresh tokens
    """
    try:
        user = AuthService.authenticate_user(db, login_data.email, login_data.password)
        
        if not user:
            logger.warning(f"Failed login attempt for: {login_data.email}")
            raise UnauthorizedError("Incorrect email or password")
        
        # Generate tokens
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})
        
        logger.info(f"User logged in successfully: {user.id}")
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
        
    except UnauthorizedError:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed. Please try again."
        )


@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_data: RefreshTokenRequest, db: Session = Depends(get_db)):
    """
    Refresh access token
    
    - Validates refresh token
    - Returns new access and refresh tokens
    """
    try:
        user_id = verify_token(refresh_data.refresh_token, "refresh")
        
        if not user_id:
            raise UnauthorizedError("Invalid refresh token")
        
        user = AuthService.get_user_by_id(db, user_id)
        
        if not user or not user.is_active:
            raise UnauthorizedError("User not found or inactive")
        
        # Generate new tokens
        access_token = create_access_token(data={"sub": str(user.id)})
        new_refresh_token = create_refresh_token(data={"sub": str(user.id)})
        
        logger.info(f"Token refreshed for user: {user.id}")
        
        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }
        
    except UnauthorizedError:
        raise
    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed"
        )


@router.get("/verify-gst/{gst_number}")
async def verify_gst_endpoint(gst_number: str):
    """
    Verify GST number
    
    - Validates GST format
    - Verifies with GST API (mock in development)
    """
    try:
        result = await verify_gst_number_api(gst_number, settings.gst_verification_api_key)
        return result
    except Exception as e:
        logger.error(f"GST verification error: {e}")
        return {
            "valid": False,
            "message": "Verification service error",
            "company_name": None,
            "status": None
        }