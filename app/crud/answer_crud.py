from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
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

async def get_answers_by_note_id( 
    note_id:int,
    db:AsyncSession = Depends(get_session)
    ):
    q = select(models.Answer).where(models.Answer.note_id == note_id)
    result = (await db.execute(q)).scalars().all()
    return result
