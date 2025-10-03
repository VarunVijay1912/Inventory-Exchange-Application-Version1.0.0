"""Enhanced authentication service"""
from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password
from app.core.logging import logger


class AuthService:
    """Authentication service with enhanced error handling"""
    
    @staticmethod
    def create_user(db: Session, user_create: UserCreate) -> User:
        """Create a new user"""
        try:
            hashed_password = get_password_hash(user_create.password)
            
            db_user = User(
                email=user_create.email,
                phone=user_create.phone,
                password_hash=hashed_password,
                company_name=user_create.company_name,
                contact_person=user_create.contact_person,
                gst_number=user_create.gst_number,
                business_license=user_create.business_license,
                address=user_create.address,
                city=user_create.city,
                state=user_create.state,
                pincode=user_create.pincode,
                user_type=user_create.user_type
            )
            
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            
            logger.info(f"User created: {db_user.id}")
            return db_user
            
        except Exception as e:
            db.rollback()
            logger.error(f"User creation error: {e}")
            raise

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """Authenticate user by email and password"""
        try:
            user = db.query(User).filter(User.email == email).first()
            
            if not user:
                logger.warning(f"Authentication failed: User not found - {email}")
                return None
            
            if not verify_password(password, user.password_hash):
                logger.warning(f"Authentication failed: Invalid password - {email}")
                return None
            
            return user
            
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return None

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_gst(db: Session, gst_number: str) -> Optional[User]:
        """Get user by GST number"""
        return db.query(User).filter(User.gst_number == gst_number).first()

    @staticmethod
    def get_user_by_phone(db: Session, phone: str) -> Optional[User]:
        """Get user by phone number"""
        return db.query(User).filter(User.phone == phone).first()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    async def verify_user_gst(db: Session, user_id: str) -> dict:
        """Verify user's GST number"""
        try:
            user = db.query(User).filter(User.id == user_id).first()
            
            if not user:
                return {"success": False, "message": "User not found"}
            
            from app.utils.validators import verify_gst_number_api
            from app.config import settings
            
            verification_result = await verify_gst_number_api(
                user.gst_number,
                settings.gst_verification_api_key
            )
            
            if verification_result["valid"]:
                user.is_verified = True
                db.commit()
                logger.info(f"User GST verified: {user.id}")
                return {"success": True, "message": "GST verified successfully"}
            
            return {"success": False, "message": "GST verification failed"}
            
        except Exception as e:
            db.rollback()
            logger.error(f"GST verification error: {e}")
            return {"success": False, "message": "Verification service error"}