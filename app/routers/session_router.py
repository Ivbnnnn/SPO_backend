from fastapi import APIRouter, Depends, File, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession
import crud
import schemas
from deps import get_session
from .auth_router import get_current_user

session_router = APIRouter(prefix="/session", tags=["session"], dependencies=[Depends(get_current_user)] )

@session_router.post('/add')
async def add_session(session:schemas.SessionCreate,db:AsyncSession = Depends(get_session)):
    session = await crud.create_session(session, db)
    await crud.create_participant(session.user_id, session.id, db)

    return session
@session_router.get('/get/participants')
async def add_session(session_id:int,db:AsyncSession = Depends(get_session)):
    participants = await crud.get_participants_by_session_id(session_id, db)

    return participants


@session_router.get('/{link}')
async def add_user(link:str,participant:schemas.ParticipantCreate,db:AsyncSession = Depends(get_session)):
    session = await crud.get_session_by_link(link, db)
    await crud.join_participant(participant=participant, db=db)

    return session