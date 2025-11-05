from fastapi import APIRouter, File, UploadFile, HTTPException, Query
from fastapi.responses import StreamingResponse
from bson import ObjectId
from typing import Optional
import logging
from datetime import datetime

from app.models.file_model import (
    FileResponse,
    FileListResponse,
    FileUpdateRequest
)
from app.services.storage import storage_service
from app.config import get_settings

router = APIRouter()
logger = logging.getLogger(__name__)
settings = get_settings()


@router.post("/upload", response_model=FileResponse, status_code=201)
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a file to storage

    Args:
        file: File to upload

    Returns:
        File metadata
    """
    try:
        # Validate file
        if not file:
            raise HTTPException(status_code=400, detail="No file provided")

        if not file.filename:
            raise HTTPException(status_code=400, detail="Invalid filename")

        # Read file data
        file_data = await file.read()
        file_size = len(file_data)

        # Check file size
        if file_size > settings.max_file_size:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Max size: {settings.max_file_size} bytes"
            )

        # Check file extension
        file_ext = file.filename.split('.')[-1].lower() if '.' in file.filename else ''
        if file_ext not in settings.allowed_extensions:
            raise HTTPException(
                status_code=415,
                detail=f"File type not allowed. Allowed: {settings.allowed_extensions}"
            )

        # Upload to MinIO
        from io import BytesIO
        minio_key = storage_service.upload_file(
            file_data=BytesIO(file_data),
            filename=file.filename,
            content_type=file.content_type or "application/octet-stream",
            file_size=file_size
        )

        # Save metadata to MongoDB
        file_metadata = {
            "name": file.filename,
            "size": file_size,
            "content_type": file.content_type or "application/octet-stream",
            "minio_key": minio_key,
            "upload_date": datetime.utcnow(),
            "owner_id": None,
            "metadata": {}
        }

        result = storage_service.files_collection.insert_one(file_metadata)

        # Return response
        return FileResponse(
            id=str(result.inserted_id),
            name=file_metadata["name"],
            size=file_metadata["size"],
            content_type=file_metadata["content_type"],
            upload_date=file_metadata["upload_date"],
            owner_id=file_metadata.get("owner_id")
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")


@router.get("", response_model=FileListResponse)
async def list_files(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = None
):
    """
    List all files with pagination and optional search

    Args:
        page: Page number (starting from 1)
        limit: Items per page
        search: Search by filename

    Returns:
        List of files with metadata
    """
    try:
        # Build query
        query = {}
        if search:
            query["name"] = {"$regex": search, "$options": "i"}

        # Get total count
        total = storage_service.files_collection.count_documents(query)

        # Get files with pagination
        skip = (page - 1) * limit
        cursor = storage_service.files_collection.find(query).sort(
            "upload_date", -1
        ).skip(skip).limit(limit)

        files = []
        for doc in cursor:
            files.append(FileResponse(
                id=str(doc["_id"]),
                name=doc["name"],
                size=doc["size"],
                content_type=doc["content_type"],
                upload_date=doc["upload_date"],
                owner_id=doc.get("owner_id")
            ))

        return FileListResponse(
            files=files,
            total=total,
            page=page,
            limit=limit
        )

    except Exception as e:
        logger.error(f"Error listing files: {e}")
        raise HTTPException(status_code=500, detail=f"Error listing files: {str(e)}")


@router.get("/{file_id}", response_model=FileResponse)
async def get_file_metadata(file_id: str):
    """
    Get file metadata by ID

    Args:
        file_id: File ID

    Returns:
        File metadata
    """
    try:
        if not ObjectId.is_valid(file_id):
            raise HTTPException(status_code=400, detail="Invalid file ID")

        doc = storage_service.files_collection.find_one({"_id": ObjectId(file_id)})

        if not doc:
            raise HTTPException(status_code=404, detail="File not found")

        return FileResponse(
            id=str(doc["_id"]),
            name=doc["name"],
            size=doc["size"],
            content_type=doc["content_type"],
            upload_date=doc["upload_date"],
            owner_id=doc.get("owner_id")
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting file metadata: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting file: {str(e)}")


@router.get("/{file_id}/download")
async def download_file(file_id: str):
    """
    Download a file

    Args:
        file_id: File ID

    Returns:
        File stream
    """
    try:
        if not ObjectId.is_valid(file_id):
            raise HTTPException(status_code=400, detail="Invalid file ID")

        doc = storage_service.files_collection.find_one({"_id": ObjectId(file_id)})

        if not doc:
            raise HTTPException(status_code=404, detail="File not found")

        # Get file from MinIO
        minio_key = doc["minio_key"]
        file_stream = storage_service.download_file(minio_key)

        # Return as streaming response
        return StreamingResponse(
            file_stream,
            media_type=doc["content_type"],
            headers={
                "Content-Disposition": f'attachment; filename="{doc["name"]}"'
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        raise HTTPException(status_code=500, detail=f"Error downloading file: {str(e)}")


@router.patch("/{file_id}", response_model=FileResponse)
async def update_file_metadata(file_id: str, update_data: FileUpdateRequest):
    """
    Update file metadata (e.g., rename)

    Args:
        file_id: File ID
        update_data: Updated metadata

    Returns:
        Updated file metadata
    """
    try:
        if not ObjectId.is_valid(file_id):
            raise HTTPException(status_code=400, detail="Invalid file ID")

        doc = storage_service.files_collection.find_one({"_id": ObjectId(file_id)})

        if not doc:
            raise HTTPException(status_code=404, detail="File not found")

        # Prepare update
        update_dict = {}
        if update_data.name is not None:
            update_dict["name"] = update_data.name

        if not update_dict:
            raise HTTPException(status_code=400, detail="No updates provided")

        # Update in MongoDB
        storage_service.files_collection.update_one(
            {"_id": ObjectId(file_id)},
            {"$set": update_dict}
        )

        # Get updated document
        updated_doc = storage_service.files_collection.find_one({"_id": ObjectId(file_id)})

        return FileResponse(
            id=str(updated_doc["_id"]),
            name=updated_doc["name"],
            size=updated_doc["size"],
            content_type=updated_doc["content_type"],
            upload_date=updated_doc["upload_date"],
            owner_id=updated_doc.get("owner_id")
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating file: {e}")
        raise HTTPException(status_code=500, detail=f"Error updating file: {str(e)}")


@router.delete("/{file_id}", status_code=204)
async def delete_file(file_id: str):
    """
    Delete a file

    Args:
        file_id: File ID
    """
    try:
        if not ObjectId.is_valid(file_id):
            raise HTTPException(status_code=400, detail="Invalid file ID")

        doc = storage_service.files_collection.find_one({"_id": ObjectId(file_id)})

        if not doc:
            raise HTTPException(status_code=404, detail="File not found")

        # Delete from MinIO
        minio_key = doc["minio_key"]
        storage_service.delete_file(minio_key)

        # Delete from MongoDB
        storage_service.files_collection.delete_one({"_id": ObjectId(file_id)})

        logger.info(f"File deleted: {file_id}")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting file: {e}")
        raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")
