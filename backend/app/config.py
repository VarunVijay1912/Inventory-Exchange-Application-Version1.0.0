import os
from typing import List
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings with validation"""
    
    # Database
    database_url: str
    
    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7
    
    # File Upload
    upload_directory: str = "./uploads"
    max_file_size: int = 10485760  # 10MB
    allowed_image_types_str: str = "jpg,jpeg,png,webp"
    
    # API Configuration
    gst_verification_api_key: str
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    # CORS
    cors_origins: str = "http://localhost:3000"
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "./logs/app.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def allowed_image_types(self) -> List[str]:
        """Parse allowed image types from string"""
        return [ext.strip() for ext in self.allowed_image_types_str.split(",")]
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from string"""
        return [origin.strip() for origin in self.cors_origins.split(",")]


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


settings = get_settings()