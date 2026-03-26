from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
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

async def update_session_note(note: schemas.SessionNoteUpdate, db: AsyncSession = Depends(get_session)):
    update_data = note.model_dump(exclude_unset=True, exclude={"id"})
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    stmt_select = select(models.Session_Note).where(models.Session_Note.id == note.id)
    db_note = (await db.execute(stmt_select)).scalars().first()

    if hasattr(note, "participant_id") and db_note.participant_id != note.participant_id:
        raise HTTPException(status_code=403, detail="You are not allowed to update this note")
    
    if not db_note:
        raise HTTPException(status_code=404, detail=f"Note with id={note.id} not found")

    stmt_update = (
        update(models.Session_Note)
        .where(models.Session_Note.id == note.id)
        .values(**update_data)
        .execution_options(synchronize_session="fetch")
    )
    
    try:
        await db.execute(stmt_update)
        await db.commit()        
        await db.refresh(db_note)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to update note: {e}")
    
    return db_note

async def delete_session_note(
    note: schemas.SessionNoteDelete,  
    db: AsyncSession = Depends(get_session)
):
    stmt_select = select(models.Session_Note).where(models.Session_Note.id == note.id)
    db_note = (await db.execute(stmt_select)).scalars().first()
    
    if not db_note:
        raise HTTPException(status_code=404, detail=f"Note with id={note.id} not found")
        
    if hasattr(note, "participant_id") and db_note.participant_id != note.participant_id:
        raise HTTPException(status_code=403, detail="You are not allowed to delete this note")
    
    stmt_delete = delete(models.Session_Note).where(models.Session_Note.id == note.id)
    
    try:
        await db.execute(stmt_delete)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete note: {e}")
    
    return note


async def get_session_notes_by_session_id(session_id:int,db:AsyncSession = Depends(get_session)):
    q = select(models.Session_Note).where(models.Session_Note.session_id == session_id)
    result = (await db.execute(q)).scalars().all()
    return result

async def get_session_notes_by_session_participant_id(session_id:int,participant_id:int, db:AsyncSession = Depends(get_session)):
    q = select(models.Session_Note).where(models.Session_Note.session_id == session_id).where(models.Session_Note.participant_id == participant_id)
    result = (await db.execute(q)).scalars().all()
    return result