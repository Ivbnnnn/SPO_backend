from fastapi import APIRouter, Depends, File, UploadFile, Form, Query
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException
import crud
import schemas
from deps import get_session
from .auth_router import get_current_user

solo_session_note_router = APIRouter(prefix="/solo_session/note", tags=["solo_session_note"], dependencies=[Depends(get_current_user)] )

@solo_session_note_router.post('/create')
async def add_session_note(solo_session_quote:schemas.SoloSessionQuoteCreate,db:AsyncSession = Depends(get_session)):
    return await crud.create_solo_session_quote(solo_session_quote, db)


@solo_session_note_router.get('/')
async def get_session_notes(
        solo_session_id:int = Query(...),
        db:AsyncSession = Depends(get_session)):
    if solo_session_id is None:
        raise HTTPException(
            status_code=422,
            detail=[
                {
                    "loc": ["solo_session_id"],
                    "msg": "solo_session_id must be provided",
                    "type": "value_error.missing"
                }
            ]
        )
    else:
        return await crud.get_solo_session_quotes_by_solo_session_id(solo_session_id, db)
  