"""Enhanced products API endpoints"""
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_verified_user, get_optional_user
from app.core.exceptions import NotFoundError, ForbiddenError, ValidationError
from app.schemas.product import Product, ProductCreate, ProductUpdate, ProductListItem
from app.models.product import Product as ProductModel
from app.models.user import User
from app.services.product_service import ProductService
from app.utils.image_processing import process_product_image
from app.config import settings
from app.core.logging import logger

router = APIRouter()


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_create: ProductCreate,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """
    Create new product listing
    
    **Requires:** Verified user
    **Returns:** Created product with details
    """
    try:
        logger.info(f"Creating product for user: {current_user.id}")
        product = ProductService.create_product(db, product_create, current_user.id)
        logger.info(f"Product created successfully: {product.id}")
        return product
    except Exception as e:
        logger.error(f"Product creation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create product"
        )


@router.get("/", response_model=List[ProductListItem])
async def list_products(
    query: Optional[str] = Query(None, description="Search query"),
    category_id: Optional[UUID] = Query(None, description="Filter by category"),
    material_id: Optional[UUID] = Query(None, description="Filter by material"),
    city: Optional[str] = Query(None, description="Filter by city"),
    state: Optional[str] = Query(None, description="Filter by state"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
    condition: Optional[str] = Query(None, description="Product condition"),
    sort_by: str = Query("created_at", description="Sort by field"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    skip: int = Query(0, ge=0, description="Skip items"),
    limit: int = Query(20, ge=1, le=100, description="Limit items"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    """
    List and search products with filters
    
    **Public endpoint** - No authentication required
    **Supports:** Search, filters, sorting, pagination
    """
    try:
        products = ProductService.search_products(
            db=db,
            query=query,
            category_id=category_id,
            material_id=material_id,
            city=city,
            state=state,
            min_price=min_price,
            max_price=max_price,
            condition=condition,
            sort_by=sort_by,
            sort_order=sort_order,
            skip=skip,
            limit=limit
        )
        
        # Convert to list items with primary image
        result = []
        for product in products:
            primary_image = next((img for img in product.images if img.is_primary), None)
            if not primary_image and product.images:
                primary_image = product.images[0]
            
            item = ProductListItem(
                id=product.id,
                title=product.title,
                price=product.price,
                price_negotiable=product.price_negotiable,
                condition=product.condition,
                location_city=product.location_city,
                location_state=product.location_state,
                views_count=product.views_count,
                status=product.status,
                created_at=product.created_at,
                primary_image=f"/uploads/products/{product.id}/medium/{primary_image.image_name}" if primary_image else None
            )
            result.append(item)
        
        logger.info(f"Retrieved {len(result)} products with filters")
        return result
        
    except Exception as e:
        logger.error(f"Product listing error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve products"
        )


@router.get("/{product_id}", response_model=Product)
async def get_product(
    product_id: UUID,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    """
    Get product details by ID
    
    **Public endpoint** - Increments view count
    """
    try:
        product = ProductService.get_product(db, product_id)
        
        if not product:
            raise NotFoundError("Product not found")
        
        # Increment views (only if not the owner viewing)
        if not current_user or current_user.id != product.seller_id:
            ProductService.increment_views(db, product_id)
        
        logger.info(f"Product retrieved: {product_id}")
        return product
        
    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Product retrieval error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve product"
        )


@router.put("/{product_id}", response_model=Product)
async def update_product(
    product_id: UUID,
    product_update: ProductUpdate,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """
    Update product details
    
    **Requires:** Product owner or admin
    """
    try:
        product = ProductService.update_product(db, product_id, product_update, current_user.id)
        
        if not product:
            raise NotFoundError("Product not found or not authorized")
        
        logger.info(f"Product updated: {product_id}")
        return product
        
    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Product update error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update product"
        )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: UUID,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """
    Delete product listing
    
    **Requires:** Product owner
    **Note:** Also deletes associated images
    """
    try:
        success = ProductService.delete_product(db, product_id, current_user.id)
        
        if not success:
            raise NotFoundError("Product not found or not authorized")
        
        # Delete associated images
        from app.utils.image_processing import delete_product_images
        delete_product_images(str(product_id), settings.upload_directory)
        
        logger.info(f"Product deleted: {product_id}")
        return None
        
    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Product deletion error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete product"
        )


@router.post("/{product_id}/images", status_code=status.HTTP_201_CREATED)
async def upload_product_images(
    product_id: UUID,
    files: List[UploadFile] = File(..., description="Product images (max 10)"),
    is_primary: Optional[bool] = Form(False, description="Mark first image as primary"),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """
    Upload product images
    
    **Requires:** Product owner
    **Limits:** Max 10 images, 10MB per file
    **Formats:** JPG, PNG, WEBP
    """
    try:
        # Verify product ownership
        product = db.query(ProductModel).filter(
            ProductModel.id == product_id,
            ProductModel.seller_id == current_user.id
        ).first()
        
        if not product:
            raise NotFoundError("Product not found or not authorized")
        
        # Check image limit
        existing_images = len(product.images)
        if existing_images + len(files) > 10:
            raise ValidationError(f"Maximum 10 images allowed. Current: {existing_images}")
        
        uploaded_images = []
        
        for i, file in enumerate(files):
            # Validate file type
            if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
                logger.warning(f"Invalid file type: {file.content_type}")
                continue
            
            # Process image
            image_data = process_product_image(
                file,
                str(product_id),
                settings.upload_directory,
                settings.max_file_size
            )
            
            # Mark first image as primary if requested
            image_data["is_primary"] = is_primary and i == 0 and existing_images == 0
            image_data["mime_type"] = file.content_type
            
            # Save to database
            db_image = ProductService.add_product_image(db, product_id, image_data)
            uploaded_images.append({
                "id": str(db_image.id),
                "filename": db_image.image_name,
                "url": f"/uploads/products/{product_id}/medium/{db_image.image_name}",
                "is_primary": db_image.is_primary
            })
        
        logger.info(f"Uploaded {len(uploaded_images)} images for product {product_id}")
        
        return {
            "success": True,
            "uploaded_count": len(uploaded_images),
            "images": uploaded_images
        }
        
    except (NotFoundError, ValidationError):
        raise
    except Exception as e:
        logger.error(f"Image upload error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload images"
        )


@router.get("/user/my-products", response_model=List[ProductListItem])
async def get_my_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status_filter: Optional[str] = Query(None, description="Filter by status"),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's products
    
    **Requires:** Authenticated user
    """
    try:
        query = db.query(ProductModel).filter(ProductModel.seller_id == current_user.id)
        
        if status_filter:
            query = query.filter(ProductModel.status == status_filter)
        
        products = query.order_by(ProductModel.created_at.desc()).offset(skip).limit(limit).all()
        
        # Convert to list items
        result = []
        for product in products:
            primary_image = next((img for img in product.images if img.is_primary), None)
            if not primary_image and product.images:
                primary_image = product.images[0]
            
            item = ProductListItem(
                id=product.id,
                title=product.title,
                price=product.price,
                price_negotiable=product.price_negotiable,
                condition=product.condition,
                location_city=product.location_city,
                location_state=product.location_state,
                views_count=product.views_count,
                status=product.status,
                created_at=product.created_at,
                primary_image=f"/uploads/products/{product.id}/medium/{primary_image.image_name}" if primary_image else None
            )
            result.append(item)
        
        logger.info(f"Retrieved {len(result)} products for user {current_user.id}")
        return result
        
    except Exception as e:
        logger.error(f"My products retrieval error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve your products"
        )