"""Enhanced validation utilities"""
import re
from typing import Optional, Dict, Any
import httpx
from app.core.logging import logger


def validate_gst_number(gst_number: str) -> bool:
    """Validate GST number format"""
    pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$'
    return bool(re.match(pattern, gst_number))


async def verify_gst_number_api(gst_number: str, api_key: str) -> Dict[str, Any]:
    """
    Verify GST number via API
    In production, replace with actual GST verification API
    """
    
    if not validate_gst_number(gst_number):
        return {
            "valid": False,
            "message": "Invalid GST format",
            "company_name": None,
            "status": None
        }
    
    # Mock API call - Replace with actual API in production
    try:
        # Example: Replace with actual GST API endpoint
        # async with httpx.AsyncClient() as client:
        #     response = await client.get(
        #         f"https://api.gst.gov.in/verify/{gst_number}",
        #         headers={"Authorization": f"Bearer {api_key}"}
        #     )
        #     data = response.json()
        #     return data
        
        # Mock response for development
        logger.info(f"GST verification requested for: {gst_number}")
        return {
            "valid": True,
            "message": "GST number verified (Mock)",
            "company_name": "Sample Company Pvt Ltd",
            "status": "Active"
        }
        
    except Exception as e:
        logger.error(f"GST verification API error: {e}")
        return {
            "valid": False,
            "message": "Verification service unavailable",
            "company_name": None,
            "status": None
        }


def validate_phone_number(phone: str) -> bool:
    """Validate Indian phone number"""
    pattern = r'^(\+91|91)?[6-9]\d{9}$'
    return bool(re.match(pattern, phone))


def validate_pincode(pincode: str) -> bool:
    """Validate Indian PIN code"""
    pattern = r'^\d{6}$'
    return bool(re.match(pattern, pincode))


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage"""
    # Remove path components
    filename = filename.split('/')[-1].split('\\')[-1]
    
    # Remove potentially dangerous characters
    filename = re.sub(r'[^\w\s.-]', '', filename)
    
    # Limit length
    max_length = 255
    if len(filename) > max_length:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = name[:max_length-len(ext)-1] + '.' + ext if ext else name[:max_length]
    
    return filename


def validate_image_file(filename: str, allowed_types: list) -> tuple[bool, str]:
    """Validate image file"""
    if not filename:
        return False, "No filename provided"
    
    # Check extension
    ext = filename.lower().split('.')[-1] if '.' in filename else ''
    
    if ext not in allowed_types:
        return False, f"Invalid file type. Allowed: {', '.join(allowed_types)}"
    
    return True, "Valid image file"