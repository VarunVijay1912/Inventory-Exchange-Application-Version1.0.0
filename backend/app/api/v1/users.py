"""Enhanced users API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_active_user
from app.core.exceptions import NotFoundError
from app.schemas.user import User, UserUpdate
from app.models.user import User as UserModel
from app.core.logging import logger

router = APIRouter()


@router.get("/me", response_model=User)
async def get_current_user_profile(
    current_user: UserModel = Depends(get_current_active_user)
):
    """
    Get current user profile
    
    **Requires:** Authenticated user
    """
    return current_user


@router.put("/me", response_model=User)
async def update_current_user(
    user_update: UserUpdate,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update current user profile
    
    **Requires:** Authenticated user
    **Note:** Cannot update email, phone, or GST number
    """
    try:
        update_data = user_update.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(current_user, field, value)
        
        db.commit()
        db.refresh(current_user)
        
        logger.info(f"User profile updated: {current_user.id}")
        return current_user
        
    except Exception as e:
        db.rollback()
        logger.error(f"Profile update error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile"
        )


@router.get("/{user_id}", response_model=User)
async def get_user_profile(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Get public user profile
    
    **Public endpoint**
    """
    try:
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        
        if not user:
            raise NotFoundError("User not found")
        
        return user
        
    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"User profile retrieval error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user profile"
        )