from fastapi import APIRouter, Depends, File, UploadFile, Form, Query
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import crud
import schemas
from deps import get_session
from .auth_router import get_current_user

answer_router = APIRouter(prefix="/answer", tags=["answer"] )

@answer_router.post('/create')
async def add_session_answer(answer:schemas.AnswerCreate,db:AsyncSession = Depends(get_session)):
    return await crud.create_answer(answer, db)



@answer_router.get('/')
async def get_session_answers(
        note_id:int = Query(...),
        db:AsyncSession = Depends(get_session)):
    return await crud.get_answers_by_note_id(note_id, db)
    