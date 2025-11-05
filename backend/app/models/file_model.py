from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic"""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")


class FileMetadata(BaseModel):
    """File metadata stored in MongoDB"""

    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(..., min_length=1, max_length=255)
    size: int = Field(..., ge=0)
    content_type: str
    minio_key: str
    upload_date: datetime = Field(default_factory=datetime.utcnow)
    owner_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class FileResponse(BaseModel):
    """Response model for file operations"""

    id: str
    name: str
    size: int
    content_type: str
    upload_date: datetime
    owner_id: Optional[str] = None

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


class FileUpdateRequest(BaseModel):
    """Request model for updating file metadata"""

    name: Optional[str] = Field(None, min_length=1, max_length=255)


class FileListResponse(BaseModel):
    """Response model for listing files"""

    files: list[FileResponse]
    total: int
    page: int
    limit: int
