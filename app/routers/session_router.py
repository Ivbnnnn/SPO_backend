from fastapi import APIRouter, Depends, File, Request, Form
from sqlalchemy.ext.asyncio import AsyncSession
import crud
import schemas, models
from deps import get_session
from .auth_router import get_current_user

session_router = APIRouter(prefix="/session", tags=["session"])

@session_router.post('/create')
async def add_session(
        session:schemas.SessionCreate,
        user:models.User = Depends(get_current_user),
        db:AsyncSession = Depends(get_session)):
    db_session = await crud.create_session(session,user.id, db)
    await crud.create_participant(user.id, db_session.id, db)

    return db_session
@session_router.get('/get/participants')
async def get_session_participants(
        session_id:int,
        user:models.User = Depends(get_current_user),
        db:AsyncSession = Depends(get_session)):
    participants = await crud.get_participants_by_session_id(session_id, db)

    return participants



@session_router.post('/notifications')
async def get_session_participants(
        session_notify:schemas.SessionNotifications,
        requst:Request,
        db:AsyncSession = Depends(get_session)):
    result = await crud.get_notifications_by_user_id(offset=session_notify.offset, limit=session_notify.limit, user_id=requst.state.user.id, db=db)

    return result


@session_router.post('/{link}', summary="Переход по ссылке добавляет участника в сессию")
async def join_by_link(
        link:str,
        request:Request,
        session_id:int,
        db:AsyncSession = Depends(get_session)):
    session = await crud.get_session_by_link(link, db)
    await crud.join_participant(request.state.user.id, session_id, db=db)

    return session