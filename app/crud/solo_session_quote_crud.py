from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import models, schemas
from sqlalchemy import select, func, cast, Float, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, Depends
from deps import get_session



# solosession quote 
async def create_solo_session_quote(
        user:models.User,
        quote:schemas.SoloSessionQuoteCreate,
        db:AsyncSession = Depends(get_session)):
    
    q_check = select(models.Solo_Session.id).where(
        models.Solo_Session.id == quote.solo_session_id,
        models.Solo_Session.user_id == user.id
    )
    db_check = (await db.execute(q_check)).scalar_one_or_none()
    if db_check is None:
        raise HTTPException(status_code=403, detail="must be auth-d")

    db_quote = models.Solo_Quote(
        **quote.model_dump()
    )
    db.add(db_quote)
    try:
        await db.commit()
        await db.refresh(db_quote)
    except HTTPException as e:
        raise HTTPException(status_code=400, detail=f'failed to create quote {e}')
    return db_quote

async def get_solo_session_quotes_by_solo_session_id(user:models.User,solo_session_id:int,db:AsyncSession = Depends(get_session)):
    q_check = select(models.Solo_Session.id).where(
        models.Solo_Session.id == solo_session_id,
        models.Solo_Session.user_id == user.id
    )
    db_check = (await db.execute(q_check)).scalar_one_or_none()
    if db_check is None:
        raise HTTPException(status_code=403, detail="must be auth-d")
    q = select(models.Solo_Quote).where(models.Solo_Quote.solo_session_id == solo_session_id)
    result = (await db.execute(q)).scalars().all()
    return result
