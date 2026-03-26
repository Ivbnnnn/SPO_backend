from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
import models, schemas
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, Depends, Form, File, UploadFile
from deps import get_session


async def create_answer( 
    answer:schemas.AnswerCreate,
    db:AsyncSession = Depends(get_session)
    ):
    db_answer = models.Answer(
        **answer.model_dump()
    )
    db.add(db_answer)
    try:
        await db.commit()
        await db.refresh(db_answer)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    return db_answer

async def update_session_answer(
        answer: schemas.AnswerUpdate,
        db: AsyncSession = Depends(get_session)):
    update_data = answer.model_dump(exclude_unset=True, exclude={"id"})
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    stmt_select = select(models.Answer).where(models.Answer.id == answer.id)
    db_answer = (await db.execute(stmt_select)).scalars().first()

    if hasattr(answer, "participant_id") and db_answer.participant_id != answer.participant_id:
        raise HTTPException(status_code=403, detail="You are not allowed to update this answer")
    
    if not db_answer:
        raise HTTPException(status_code=404, detail=f"Answer with id={answer.id} not found")

    stmt_update = (
        update(models.Answer)
        .where(models.Answer.id == answer.id)
        .values(**update_data)
        .execution_options(synchronize_session="fetch")
    )
    
    try:
        await db.execute(stmt_update)
        await db.commit()        
        await db.refresh(db_answer)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to update answer: {e}")
    
    return db_answer



async def delete_session_answer(
    answer: schemas.AnswerDelete,  
    db: AsyncSession = Depends(get_session)
):
    stmt_select = select(models.Answer).where(models.Answer.id == answer.id)
    db_answer = (await db.execute(stmt_select)).scalars().first()
    
    if not db_answer:
        raise HTTPException(status_code=404, detail=f"Answer with id={answer.id} not found")
        
    if hasattr(answer, "participant_id") and db_answer.participant_id != answer.participant_id:
        raise HTTPException(status_code=403, detail="You are not allowed to delete this answer")
    
    stmt_delete = delete(models.Answer).where(models.Answer.id == answer.id)
    
    try:
        await db.execute(stmt_delete)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete answer: {e}")
    
    return answer



async def get_answers_by_note_id( 
    note_id:int,
    db:AsyncSession = Depends(get_session)
    ):
    q = select(models.Answer).where(models.Answer.note_id == note_id)
    result = (await db.execute(q)).scalars().all()
    return result
