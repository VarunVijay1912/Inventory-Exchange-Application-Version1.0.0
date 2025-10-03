"""Enhanced admin panel API endpoints"""
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.dependencies import get_db, get_current_active_user
from app.core.exceptions import NotFoundError, ForbiddenError
from app.schemas.user import User
from app.models.user import User as UserModel
from app.models.product import Product as ProductModel
from app.models.conversation import Conversation, Message
from app.core.logging import logger

router = APIRouter()


def verify_admin(current_user: UserModel = Depends(get_current_active_user)):
    """Verify user is admin - for MVP, any verified user can access admin"""
    # TODO: Implement proper admin role checking
    if not current_user.is_verified:
        raise ForbiddenError("Admin access denied")
    return current_user


@router.get("/dashboard")
async def admin_dashboard(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(verify_admin)
):
    """
    Get admin dashboard statistics
    
    **Requires:** Admin access
    **Returns:** Platform metrics and KPIs
    """
    try:
        # User statistics
        total_users = db.query(func.count(UserModel.id)).scalar()
        verified_users = db.query(func.count(UserModel.id)).filter(
            UserModel.is_verified == True
        ).scalar()
        active_users = db.query(func.count(UserModel.id)).filter(
            UserModel.is_active == True
        ).scalar()
        
        # Product statistics
        total_products = db.query(func.count(ProductModel.id)).scalar()
        active_products = db.query(func.count(ProductModel.id)).filter(
            ProductModel.is_active == True,
            ProductModel.status == "active"
        ).scalar()
        sold_products = db.query(func.count(ProductModel.id)).filter(
            ProductModel.status == "sold"
        ).scalar()
        
        # Conversation statistics
        total_conversations = db.query(func.count(Conversation.id)).scalar()
        total_messages = db.query(func.count(Message.id)).scalar()
        
        # Recent activity (last 30 days)
        from datetime import datetime, timedelta
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        new_users_30d = db.query(func.count(UserModel.id)).filter(
            UserModel.created_at >= thirty_days_ago
        ).scalar()
        
        new_products_30d = db.query(func.count(ProductModel.id)).filter(
            ProductModel.created_at >= thirty_days_ago
        ).scalar()
        
        dashboard_data = {
            "users": {
                "total": total_users,
                "verified": verified_users,
                "active": active_users,
                "pending_verification": total_users - verified_users,
                "new_last_30_days": new_users_30d
            },
            "products": {
                "total": total_products,
                "active": active_products,
                "sold": sold_products,
                "inactive": total_products - active_products - sold_products,
                "new_last_30_days": new_products_30d
            },
            "engagement": {
                "total_conversations": total_conversations,
                "total_messages": total_messages,
                "avg_messages_per_conversation": round(
                    total_messages / total_conversations if total_conversations > 0 else 0, 2
                )
            }
        }
        
        logger.info(f"Admin dashboard accessed by: {current_user.id}")
        return dashboard_data
        
    except Exception as e:
        logger.error(f"Admin dashboard error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load dashboard"
        )


@router.get("/users", response_model=List[User])
async def list_users_admin(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    verified: Optional[bool] = Query(None),
    active: Optional[bool] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(verify_admin)
):
    """
    List all users with filters
    
    **Requires:** Admin access
    **Supports:** Filtering by verification status, active status, search
    """
    try:
        query = db.query(UserModel)
        
        if verified is not None:
            query = query.filter(UserModel.is_verified == verified)
        
        if active is not None:
            query = query.filter(UserModel.is_active == active)
        
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                (UserModel.company_name.ilike(search_pattern)) |
                (UserModel.email.ilike(search_pattern)) |
                (UserModel.gst_number.ilike(search_pattern))
            )
        
        users = query.order_by(UserModel.created_at.desc()).offset(skip).limit(limit).all()
        
        logger.info(f"Admin retrieved {len(users)} users")
        return users
        
    except Exception as e:
        logger.error(f"Admin user list error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve users"
        )


@router.put("/users/{user_id}/verify")
async def verify_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(verify_admin)
):
    """
    Verify a user account
    
    **Requires:** Admin access
    **Action:** Sets is_verified to True
    """
    try:
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        
        if not user:
            raise NotFoundError("User not found")
        
        user.is_verified = True
        db.commit()
        
        logger.info(f"User verified by admin: {user_id}")
        return {
            "success": True,
            "message": "User verified successfully",
            "user_id": str(user_id)
        }
        
    except NotFoundError:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"User verification error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to verify user"
        )


@router.put("/users/{user_id}/deactivate")
async def deactivate_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(verify_admin)
):
    """
    Deactivate a user account
    
    **Requires:** Admin access
    **Action:** Sets is_active to False
    """
    try:
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        
        if not user:
            raise NotFoundError("User not found")
        
        user.is_active = False
        db.commit()
        
        logger.info(f"User deactivated by admin: {user_id}")
        return {
            "success": True,
            "message": "User deactivated successfully",
            "user_id": str(user_id)
        }
        
    except NotFoundError:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"User deactivation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to deactivate user"
        )


@router.put("/users/{user_id}/activate")
async def activate_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(verify_admin)
):
    """
    Activate a user account
    
    **Requires:** Admin access
    **Action:** Sets is_active to True
    """
    try:
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        
        if not user:
            raise NotFoundError("User not found")
        
        user.is_active = True
        db.commit()
        
        logger.info(f"User activated by admin: {user_id}")
        return {
            "success": True,
            "message": "User activated successfully",
            "user_id": str(user_id)
        }
        
    except NotFoundError:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"User activation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to activate user"
        )


@router.get("/products")
async def list_products_admin(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status_filter: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(verify_admin)
):
    """
    List all products for moderation
    
    **Requires:** Admin access
    """
    try:
        query = db.query(ProductModel)
        
        if status_filter:
            query = query.filter(ProductModel.status == status_filter)
        
        products = query.order_by(ProductModel.created_at.desc()).offset(skip).limit(limit).all()
        
        logger.info(f"Admin retrieved {len(products)} products")
        return products
        
    except Exception as e:
        logger.error(f"Admin product list error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve products"
        )