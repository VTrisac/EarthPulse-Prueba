from minio import Minio
from minio.error import S3Error
from pymongo import MongoClient
from pymongo.collection import Collection
from datetime import datetime, timedelta
import uuid
import logging
from typing import Optional, BinaryIO

from app.config import get_settings

logger = logging.getLogger(__name__)


class StorageService:
    """Service for managing file storage with MinIO and MongoDB"""

    def __init__(self):
        self.settings = get_settings()
        self.minio_client: Optional[Minio] = None
        self.mongo_client: Optional[MongoClient] = None
        self.db = None
        self.files_collection: Optional[Collection] = None

    def initialize(self):
        """Initialize MinIO and MongoDB connections"""
        # Initialize MinIO
        try:
            self.minio_client = Minio(
                self.settings.minio_endpoint,
                access_key=self.settings.minio_access_key,
                secret_key=self.settings.minio_secret_key,
                secure=self.settings.minio_secure
            )

            # Create bucket if it doesn't exist
            if not self.minio_client.bucket_exists(self.settings.minio_bucket):
                self.minio_client.make_bucket(self.settings.minio_bucket)
                logger.info(f"Created bucket: {self.settings.minio_bucket}")
            else:
                logger.info(f"Bucket already exists: {self.settings.minio_bucket}")

        except S3Error as e:
            logger.error(f"MinIO initialization error: {e}")
            raise

        # Initialize MongoDB
        try:
            self.mongo_client = MongoClient(self.settings.mongo_url)
            self.db = self.mongo_client[self.settings.mongo_db_name]
            self.files_collection = self.db["files"]

            # Create indexes
            self.files_collection.create_index("name")
            self.files_collection.create_index([("upload_date", -1)])
            logger.info("MongoDB initialized successfully")

        except Exception as e:
            logger.error(f"MongoDB initialization error: {e}")
            raise

    def generate_minio_key(self, filename: str) -> str:
        """Generate unique MinIO object key"""
        date_path = datetime.utcnow().strftime("%Y/%m/%d")
        unique_id = str(uuid.uuid4())
        return f"files/{date_path}/{unique_id}-{filename}"

    def upload_file(
        self,
        file_data: BinaryIO,
        filename: str,
        content_type: str,
        file_size: int
    ) -> str:
        """
        Upload file to MinIO

        Args:
            file_data: File binary data
            filename: Original filename
            content_type: MIME type
            file_size: Size in bytes

        Returns:
            MinIO object key
        """
        try:
            minio_key = self.generate_minio_key(filename)

            self.minio_client.put_object(
                bucket_name=self.settings.minio_bucket,
                object_name=minio_key,
                data=file_data,
                length=file_size,
                content_type=content_type
            )

            logger.info(f"File uploaded to MinIO: {minio_key}")
            return minio_key

        except S3Error as e:
            logger.error(f"Error uploading to MinIO: {e}")
            raise

    def download_file(self, minio_key: str):
        """
        Download file from MinIO

        Args:
            minio_key: MinIO object key

        Returns:
            File stream
        """
        try:
            response = self.minio_client.get_object(
                bucket_name=self.settings.minio_bucket,
                object_name=minio_key
            )
            return response

        except S3Error as e:
            logger.error(f"Error downloading from MinIO: {e}")
            raise

    def delete_file(self, minio_key: str):
        """
        Delete file from MinIO

        Args:
            minio_key: MinIO object key
        """
        try:
            self.minio_client.remove_object(
                bucket_name=self.settings.minio_bucket,
                object_name=minio_key
            )
            logger.info(f"File deleted from MinIO: {minio_key}")

        except S3Error as e:
            logger.error(f"Error deleting from MinIO: {e}")
            raise

    def get_presigned_url(self, minio_key: str, expires: timedelta = timedelta(minutes=15)) -> str:
        """
        Generate presigned URL for file download

        Args:
            minio_key: MinIO object key
            expires: URL expiration time

        Returns:
            Presigned URL
        """
        try:
            url = self.minio_client.get_presigned_url(
                "GET",
                self.settings.minio_bucket,
                minio_key,
                expires=expires
            )
            return url

        except S3Error as e:
            logger.error(f"Error generating presigned URL: {e}")
            raise

    def close(self):
        """Close connections"""
        if self.mongo_client:
            self.mongo_client.close()
            logger.info("MongoDB connection closed")


# Global storage service instance
storage_service = StorageService()
