from fastapi import APIRouter, Depends, File, UploadFile, Form, Query
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException
import crud
import schemas
from deps import get_session
from .auth_router import get_current_user

session_note_router = APIRouter(prefix="/session/note", tags=["session_note"], dependencies=[Depends(get_current_user)] )

@session_note_router.post('/create')
async def add_session_note(
        session_note:schemas.SessionNoteCreate,
        db:AsyncSession = Depends(get_session)):
    return await crud.create_session_note(session_note, db)


@session_note_router.get('/')
async def get_session_notes(
        session_id:int | None = Query(default=None),
        participant_id:int | None = Query(default=None),
        db:AsyncSession = Depends(get_session)):
    if session_id is None and participant_id is None:
        raise HTTPException(
            status_code=422,
            detail=[
                {
                    "loc": ["query", "session_id"],
                    "msg": "either session_id or participant_id must be provided",
                    "type": "value_error.missing"
                }
            ]
        )

    if session_id is not None and participant_id is None:
        return await crud.get_session_notes_by_session_id(session_id, db)
    elif session_id is not None and participant_id is not None:
        return await crud.get_session_notes_by_session_participant_id(session_id, participant_id, db)
