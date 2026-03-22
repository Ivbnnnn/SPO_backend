# app/minio_api.py
import io
import uuid
import logging
from fastapi import APIRouter, UploadFile, File, Depends, Form, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.concurrency import run_in_threadpool

from deps import get_session
import models, schemas
from minio import Minio

logger = logging.getLogger(__name__)

router = APIRouter()

client = Minio(
    "minio:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

bucket_name = "images"

# Проверяем бакет при импорте (или перенести в startup)
try:
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
        logger.info("Created MinIO bucket %s", bucket_name)
except Exception:
    logger.exception("Failed to ensure MinIO bucket exists")


@router.get("/images/{object_name}", tags=["Minio"])
async def proxy(object_name: str):        
    data = client.get_object("images", object_name)
    # data is a stream; wrap in StreamingResponse
    return StreamingResponse(data, media_type="image/jpeg")



async def upload_book_to_minio(
    file: UploadFile = File(...)
):
    # Прочитать файл
    contents = await file.read()

    # Генерим уникальное имя, чтобы не затирать
    ext = ""
    if "." in file.filename:
        ext = "." + file.filename.rsplit(".", 1)[1]
    filename = f"{uuid.uuid4().hex}{ext}"

    file_obj = io.BytesIO(contents)
    file_obj.seek(0)

    # Загружаем в MinIO (в потоке)
    try:
        await run_in_threadpool(
            client.put_object,
            bucket_name,
            filename,
            file_obj,
            length=len(contents),
        )
    except Exception as e:
        logger.exception("MinIO upload failed")
        raise HTTPException(status_code=500, detail="Failed to upload file to MinIO")

    file_url = f"{filename}"

    return file_url

async def delete_book_from_minio(
        file_name:str
):
    try:
        await run_in_threadpool(
            client.remove_object,
            bucket_name,
            file_name
        )
    except Exception as e:
        logger.exception("MinIO upload failed")
        raise HTTPException(status_code=500, detail=f"Failed to delete file from MinIO")