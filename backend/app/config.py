import os
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings from environment variables"""

    # MongoDB
    mongo_url: str = os.getenv("MONGO_URL", "mongodb://mongo:27017/filesdb")
    mongo_db_name: str = "filesdb"

    # MinIO
    minio_endpoint: str = os.getenv("MINIO_ENDPOINT", "minio:9000")
    minio_access_key: str = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    minio_secret_key: str = os.getenv("MINIO_SECRET_KEY", "minioadmin")
    minio_bucket: str = os.getenv("MINIO_BUCKET", "files")
    minio_secure: bool = os.getenv("MINIO_SECURE", "false").lower() == "true"

    # File upload settings
    max_file_size: int = 200 * 1024 * 1024  # 200 MB
    allowed_extensions: set = {
        "pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx",
        "txt", "jpg", "jpeg", "png", "gif", "zip", "rar", "mp4", "mp3"
    }

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
