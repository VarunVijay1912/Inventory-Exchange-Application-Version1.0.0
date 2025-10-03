"""Enhanced image processing utilities"""
import os
import uuid
from pathlib import Path
from typing import Dict, Optional
from PIL import Image
from fastapi import UploadFile
from app.core.logging import logger
from app.core.exceptions import ValidationError

# Image size configurations
THUMBNAIL_SIZE = (200, 200)
MEDIUM_SIZE = (800, 600)
MAX_ORIGINAL_SIZE = (2000, 2000)


def create_directory(path: str) -> None:
    """Create directory if it doesn't exist"""
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logger.error(f"Failed to create directory {path}: {e}")
        raise


def validate_image_size(file: UploadFile, max_size: int) -> None:
    """Validate image file size"""
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset to beginning
    
    if file_size > max_size:
        raise ValidationError(f"File size exceeds maximum allowed size of {max_size / 1024 / 1024}MB")


def optimize_image(image: Image.Image, max_size: tuple, quality: int = 85) -> Image.Image:
    """Optimize image size and quality"""
    # Convert RGBA to RGB if necessary
    if image.mode in ("RGBA", "P", "LA"):
        # Create white background
        background = Image.new("RGB", image.size, (255, 255, 255))
        if image.mode == "P":
            image = image.convert("RGBA")
        background.paste(image, mask=image.split()[-1] if image.mode == "RGBA" else None)
        image = background
    elif image.mode != "RGB":
        image = image.convert("RGB")
    
    # Resize if larger than max size
    image.thumbnail(max_size, Image.Resampling.LANCZOS)
    
    return image


def process_product_image(
    file: UploadFile,
    product_id: str,
    upload_dir: str,
    max_file_size: int
) -> Dict[str, any]:
    """
    Process and save product image with multiple sizes
    Returns dict with file paths and metadata
    """
    try:
        # Validate file size
        validate_image_size(file, max_file_size)
        
        # Generate unique filename
        file_extension = file.filename.split('.')[-1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        
        # Create directory structure
        product_dir = os.path.join(upload_dir, "products", product_id)
        original_dir = os.path.join(product_dir, "original")
        medium_dir = os.path.join(product_dir, "medium")
        thumb_dir = os.path.join(product_dir, "thumbnail")
        
        for directory in [original_dir, medium_dir, thumb_dir]:
            create_directory(directory)
        
        # Read image
        file_content = file.file.read()
        original_path = os.path.join(original_dir, unique_filename)
        
        # Save original (optimized)
        with Image.open(file.file) as img:
            # Optimize original
            img_optimized = optimize_image(img.copy(), MAX_ORIGINAL_SIZE, quality=90)
            img_optimized.save(original_path, optimize=True, quality=90)
            
            # Create medium size
            img_medium = optimize_image(img.copy(), MEDIUM_SIZE, quality=85)
            medium_path = os.path.join(medium_dir, unique_filename)
            img_medium.save(medium_path, optimize=True, quality=85)
            
            # Create thumbnail
            img_thumb = optimize_image(img.copy(), THUMBNAIL_SIZE, quality=80)
            thumb_path = os.path.join(thumb_dir, unique_filename)
            img_thumb.save(thumb_path, optimize=True, quality=80)
        
        file_size = os.path.getsize(original_path)
        
        logger.info(f"Successfully processed image for product {product_id}: {unique_filename}")
        
        return {
            "filename": unique_filename,
            "original_path": original_path,
            "medium_path": medium_path,
            "thumbnail_path": thumb_path,
            "file_size": file_size,
            "content_type": file.content_type
        }
        
    except ValidationError:
        raise
    except Exception as e:
        logger.error(f"Image processing error: {e}")
        raise ValidationError(f"Failed to process image: {str(e)}")


def delete_product_images(product_id: str, upload_dir: str) -> None:
    """Delete all images for a product"""
    try:
        product_dir = os.path.join(upload_dir, "products", product_id)
        if os.path.exists(product_dir):
            import shutil
            shutil.rmtree(product_dir)
            logger.info(f"Deleted images for product {product_id}")
    except Exception as e:
        logger.error(f"Failed to delete images for product {product_id}: {e}")