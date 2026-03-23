from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import models, schemas
from sqlalchemy import select, func, cast, Float, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, Depends
from deps import get_session



async def create_session_quote(quote:schemas.SessionQuoteCreate,db:AsyncSession = Depends(get_session)):
    db_quote = models.Session_Quote(
        **quote.model_dump()
    )
    db.add(db_quote)
    try:
        await db.commit()
        await db.refresh(db_quote)
    except HTTPException as e:
        raise HTTPException(status_code=400, detail=f'failed to create quote {e}')
    return db_quote

async def get_session_quotes_by_session_id(session_id:int,db:AsyncSession = Depends(get_session)):
    q = select(models.Session_Quote).where(models.Session_Quote.session_id == session_id)
    result = (await db.execute(q)).scalars().all()
    return result

async def get_session_quotes_by_session_participant_id(session_id:int,participant_id:int, db:AsyncSession = Depends(get_session)):
    q = select(models.Session_Quote).where(models.Session_Quote.session_id == session_id).where(models.Session_Quote.participant_id == participant_id)
    result = (await db.execute(q)).scalars().all()
    return result