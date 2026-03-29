from fastapi import APIRouter, Depends, File, UploadFile, Form, Query
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import crud
import schemas, models
from deps import get_session
from .auth_router import get_current_user

solo_session_router = APIRouter(prefix="/solo_session", tags=["solo_session"])

@solo_session_router.post('/create')
async def create_solo_session(
    book_id:int = Query(...),
    user:models.User = Depends(get_current_user),
    db:AsyncSession = Depends(get_session)):
    return await crud.create_solo_session(user,book_id, db)



@solo_session_router.get('/')
async def get_solo_session(
        user:models.User = Depends(get_current_user),
        book_id:int = Query(None),
        db:AsyncSession = Depends(get_session)):
    return await crud.get_solo_session(user.id,book_id, db)
    