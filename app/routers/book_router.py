from fastapi import APIRouter, Depends, File, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession
import crud
import schemas
from deps import get_session


book_router = APIRouter(prefix="/book", tags=["book"])


@book_router.post('/add', response_model=schemas.BookRead)
async def add_book(
    title:str = Form(...),
    author:str = Form(...),
    user_id:int = Form(...),
    book_cover:UploadFile = File(...),
    content:UploadFile = File(...),
    db:AsyncSession = Depends(get_session)
    ):
    return await crud.create_book(title,author ,user_id,book_cover,content, db)

@book_router.get('/get', response_model=schemas.BookRead)
async def add_book(
    title:str = Form(...),
    author:str = Form(...),
    user_id:int = Form(...),
    book_cover:UploadFile = File(...),
    content:UploadFile = File(...),
    db:AsyncSession = Depends(get_session)
    ):
    return await crud.create_book(title,author ,user_id,book_cover,content, db)

@book_router.patch('/update', response_model=schemas.BookRead)
async def add_book(
    title:str = Form(...),
    author:str = Form(...),
    user_id:int = Form(...),
    book_cover:UploadFile = File(...),
    content:UploadFile = File(...),
    db:AsyncSession = Depends(get_session)
    ):
    return await crud.create_book(title,author ,user_id,book_cover,content, db)

@book_router.delete('/delete', response_model=schemas.BookRead)
async def add_book(
    title:str = Form(...),
    author:str = Form(...),
    user_id:int = Form(...),
    book_cover:UploadFile = File(...),
    content:UploadFile = File(...),
    db:AsyncSession = Depends(get_session)
    ):
    return await crud.create_book(title,author ,user_id,book_cover,content, db)