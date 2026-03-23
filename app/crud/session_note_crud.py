from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import models, schemas
from sqlalchemy import select, func, cast, Float, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, Depends
from deps import get_session



# session note notes
async def create_session_note(note:schemas.SessionNoteCreate,db:AsyncSession = Depends(get_session)):
    db_note = models.Session_Note(
        **note.model_dump()
    )
    db.add(db_note)
    try:
        await db.commit()
        await db.refresh(db_note)
    except HTTPException as e:
        raise HTTPException(status_code=400, detail=f'failed to create note {e}')
    return db_note

async def get_session_notes_by_session_id(session_id:int,db:AsyncSession = Depends(get_session)):
    q = select(models.Session_Note).where(models.Session_Note.session_id == session_id)
    result = (await db.execute(q)).scalars().all()
    return result

async def get_session_notes_by_session_participant_id(session_id:int,participant_id:int, db:AsyncSession = Depends(get_session)):
    q = select(models.Session_Note).where(models.Session_Note.session_id == session_id).where(models.Session_Note.participant_id == participant_id)
    result = (await db.execute(q)).scalars().all()
    return result