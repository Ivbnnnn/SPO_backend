from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
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

async def update_session_quote(quote: schemas.SessionQuoteUpdate, db: AsyncSession = Depends(get_session)):
    update_data = quote.model_dump(exclude_unset=True, exclude={"id"})
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    stmt_select = select(models.Session_Quote).where(models.Session_Quote.id == quote.id)
    db_quote = (await db.execute(stmt_select)).scalars().first()

    if hasattr(quote, "participant_id") and db_quote.participant_id != quote.participant_id:
        raise HTTPException(status_code=403, detail="You are not allowed to update this quote")
    
    if not db_quote:
        raise HTTPException(status_code=404, detail=f"Quote with id={quote.id} not found")

    stmt_update = (
        update(models.Session_Quote)
        .where(models.Session_Quote.id == quote.id)
        .values(**update_data)
        .execution_options(synchronize_session="fetch")
    )
    
    try:
        await db.execute(stmt_update)
        await db.commit()        
        await db.refresh(db_quote)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to update quote: {e}")
    
    return db_quote

async def delete_session_quote(
    quote: schemas.SessionQuoteDelete,  
    db: AsyncSession = Depends(get_session)
):
    stmt_select = select(models.Session_Quote).where(models.Session_Quote.id == quote.id)
    db_quote = (await db.execute(stmt_select)).scalars().first()
    
    if not db_quote:
        raise HTTPException(status_code=404, detail=f"Quote with id={quote.id} not found")
        
    if hasattr(quote, "participant_id") and db_quote.participant_id != quote.participant_id:
        raise HTTPException(status_code=403, detail="You are not allowed to delete this quote")
    
    stmt_delete = delete(models.Session_Quote).where(models.Session_Quote.id == quote.id)
    
    try:
        await db.execute(stmt_delete)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete quote: {e}")
    
    return quote


async def get_session_quotes_by_session_id(session_id:int,db:AsyncSession = Depends(get_session)):
    q = select(models.Session_Quote).where(models.Session_Quote.session_id == session_id)
    result = (await db.execute(q)).scalars().all()
    return result

async def get_session_quotes_by_session_participant_id(session_id:int,participant_id:int, db:AsyncSession = Depends(get_session)):
    q = select(models.Session_Quote).where(models.Session_Quote.session_id == session_id).where(models.Session_Quote.participant_id == participant_id)
    result = (await db.execute(q)).scalars().all()
    return result