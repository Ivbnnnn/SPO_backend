from fastapi import APIRouter, Depends, File, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession
import crud
import schemas
from deps import get_session


user_router = APIRouter(prefix="/user", tags=["user"])

@user_router.post('/add', response_model=schemas.UserCreate)
async def add_user(user:schemas.UserCreate,db:AsyncSession = Depends(get_session)):
    return await crud.create_user(user, db)