# app/minio_api.py
import io
import uuid
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from fastapi.responses import StreamingResponse, JSONResponse
from starlette.concurrency import run_in_threadpool
import json
from minio import Minio
from fastapi import UploadFile, File, HTTPException
from bs4 import BeautifulSoup
from ebooklib import epub, ITEM_DOCUMENT
from tempfile import NamedTemporaryFile
import os


logger = logging.getLogger(__name__)

minio_router = APIRouter()


client = Minio(
    "minio:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

bucket_name = "books"

# Проверяем бакет при импорте (или перенести в startup)
try:
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
        logger.info("Created MinIO bucket %s", bucket_name)
except Exception:
    logger.exception("Failed to ensure MinIO bucket exists")

#routes
@minio_router.get("/books/cover/{object_name}", tags=["Minio"])
async def proxy(object_name: str):        
    data = client.get_object("books", object_name)    
    return StreamingResponse(data, media_type="image/jpeg")


@minio_router.get("/books/content/{object_name}", tags=["Minio"])
async def proxy(object_name: str,offset: int = Query(0, ge=0), limit: int = Query(10, ge=1)):        
    try:
        response = client.get_object(bucket_name, object_name)
        content_bytes = response.read()
        response.close()
        response.release_conn()

        data = json.loads(content_bytes)

        sorted_keys = sorted(data.keys(), key=lambda k: int(k))
        paginated_data = {}

        for i, key in enumerate(sorted_keys[offset:offset+limit], start=offset+1):
            paginated_data[key] = data[key]

        return JSONResponse(paginated_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read object: {str(e)}")



#help funcs

def split_text_into_chunks(text: str, chunk_size: int = 3000) -> dict[str, str]:
    chunks = {}
    page = 1

    for i in range(0, len(text), chunk_size):
        chunks[str(page)] = text[i:i + chunk_size]
        page += 1

    return chunks


def extract_text_from_epub(epub_path: str) -> str:
    book = epub.read_epub(epub_path)
    parts = []

    for item in book.get_items_of_type(ITEM_DOCUMENT):
        html = item.get_content()
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(" ", strip=True)
        if text:
            parts.append(text)

    return "\n".join(parts)

async def upload_book_to_minio(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="File name is missing")
    if not file.filename.lower().endswith(".epub"):
        raise HTTPException(status_code=400, detail="Only .epub files are allowed")
    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Empty file")
    tmp_path = None
    try:
        with NamedTemporaryFile(delete=False, suffix=".epub") as tmp:
            tmp.write(contents)
            tmp_path = tmp.name

        text = extract_text_from_epub(tmp_path)

        if not text.strip():
            raise HTTPException(status_code=400, detail="No text found in EPUB")

        chunks = split_text_into_chunks(text, chunk_size=3000)

        json_bytes = json.dumps(
            chunks,
            ensure_ascii=False,
            indent=2
        ).encode("utf-8")

        json_filename = f"{uuid.uuid4().hex}.json"

        file_obj = io.BytesIO(json_bytes)
        file_obj.seek(0)

        await run_in_threadpool(
            client.put_object,
            bucket_name,
            json_filename,
            file_obj,
            length=len(json_bytes),
            
        )
        return tmp_path

    except HTTPException:
        raise
    except Exception as e:
        print("UNEXPECTED ERROR:", repr(e))

        raise HTTPException(status_code=500, detail="Failed to parse EPUB file")
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
            print("tmp removed")



async def upload_cover_to_minio(
    file: UploadFile = File(...)
):
    contents = await file.read()


    ext = ""
    if "." in file.filename:
        ext = "." + file.filename.rsplit(".", 1)[1]
    filename = f"{uuid.uuid4().hex}{ext}"

    file_obj = io.BytesIO(contents)
    file_obj.seek(0)
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