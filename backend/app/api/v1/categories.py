"""Categories and materials API endpoints"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.schemas.category import Category, Material
from app.models.category import Category as CategoryModel, Material as MaterialModel
from app.core.logging import logger

router = APIRouter()


@router.get("/", response_model=List[Category])
async def list_categories(db: Session = Depends(get_db)):
    """
    List all active categories
    
    **Public endpoint**
    """
    try:
        categories = db.query(CategoryModel).filter(
            CategoryModel.is_active == True
        ).order_by(CategoryModel.name).all()
        
        logger.info(f"Retrieved {len(categories)} categories")
        return categories
        
    except Exception as e:
        logger.error(f"Categories retrieval error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve categories"
        )


@router.get("/materials", response_model=List[Material])
async def list_materials(db: Session = Depends(get_db)):
    """
    List all active materials
    
    **Public endpoint**
    """
    try:
        materials = db.query(MaterialModel).filter(
            MaterialModel.is_active == True
        ).order_by(MaterialModel.name).all()
        
        logger.info(f"Retrieved {len(materials)} materials")
        return materials
        
    except Exception as e:
        logger.error(f"Materials retrieval error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve materials"
        )