from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import models, schemas
from sqlalchemy import select, func, cast, Float, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, Depends
from deps import get_session



# solosession note 
async def create_solo_session_note(note:schemas.SoloSessionNoteCreate,db:AsyncSession = Depends(get_session)):
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

async def get_solo_session_notes_by_solo_session_id(solo_session_id:int,db:AsyncSession = Depends(get_session)):
    q = select(models.Session_Note).where(models.Solo_Note.solo_session_id == solo_session_id)
    result = (await db.execute(q)).scalars().all()
    return result
