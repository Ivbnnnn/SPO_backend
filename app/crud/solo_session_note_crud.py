from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
import models, schemas
from sqlalchemy import select, func, cast, Float, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, Depends
from deps import get_session



# solosession note 
async def create_solo_session_note(
        user:models.User,
        note:schemas.SoloSessionNoteCreate,
        db:AsyncSession = Depends(get_session)):
    q_check = select(models.Solo_Session.id).where(
        models.Solo_Session.id == note.solo_session_id,
        models.Solo_Session.user_id == user.id
    )
    db_check = (await db.execute(q_check)).scalar_one_or_none()
    if db_check is None:
        raise HTTPException(status_code=403, detail="must be auth-d")

    db_note = models.Solo_Note(
        **note.model_dump()
    )
    db.add(db_note)
    try:
        await db.commit()
        await db.refresh(db_note)
    except HTTPException as e:
        raise HTTPException(status_code=400, detail=f'failed to create note {e}')
    return db_note


async def update_solo_session_note(
        user:models.User,
        note:schemas.SoloSessionNoteUpdate,
        db:AsyncSession = Depends(get_session)):
    q_check = select(models.Solo_Session.id).where(
        models.Solo_Session.id == note.solo_session_id,
        models.Solo_Session.user_id == user.id
    )
    db_check = (await db.execute(q_check)).scalar_one_or_none()
    if db_check is None:
        raise HTTPException(status_code=403, detail="must be auth-d")
    update_data = note.model_dump(exclude_unset=True, exclude={"id"})
    update_stmt = update(models.Solo_Note).where(models.Solo_Note.id == note.id).values(update_data).execution_options(synchronize_session="fetch")
    try:
        db_note = (await db.execute(update_stmt)).scalar_one_or_none()
        await db.commit()
        await db.refresh(db_note)
    except HTTPException as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f'failed to create note {e}')
    return db_note


async def delete_solo_session_note(
        user:models.User,
        note:schemas.SoloSessionNoteUpdate,
        db:AsyncSession = Depends(get_session)):
    q_check = select(models.Solo_Session.id).where(
        models.Solo_Session.id == note.solo_session_id,
        models.Solo_Session.user_id == user.id
    )
    db_check = (await db.execute(q_check)).scalar_one_or_none()
    if db_check is None:
        raise HTTPException(status_code=403, detail="must be auth-d")
    db_note = (await db.execute(select(models.Solo_Note).where(models.Solo_Note.id == note.id))).scalar_one_or_none()
    if db_note is None:
        raise HTTPException(status_code=404, detail="solo not not found")
    delete_stmt = delete(models.Solo_Note).where(models.Solo_Note.id == note.id)
    try:
        (await db.execute(delete_stmt)).scalar_one_or_none()
        await db.commit()
    except HTTPException as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f'failed to delete note {e}')
    return note

async def get_solo_session_notes_by_solo_session_id(user:models.User,solo_session_id:int,db:AsyncSession = Depends(get_session)):
    q_check = select(models.Solo_Session.id).where(
        models.Solo_Session.id == solo_session_id,
        models.Solo_Session.user_id == user.id
    )
    db_check = (await db.execute(q_check)).scalar_one_or_none()
    if db_check is None:
        raise HTTPException(status_code=403, detail="must be auth-d")
    
    q = select(models.Solo_Note).where(models.Solo_Note.solo_session_id == solo_session_id)
    result = (await db.execute(q)).scalars().all()
    return result
