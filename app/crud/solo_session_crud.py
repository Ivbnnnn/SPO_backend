from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import models, schemas
from sqlalchemy import select, func, cast, Float, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, Depends, Query
from deps import get_session
from passlib.context import CryptContext
import uuid

# Session

async def create_solo_session(session:schemas.SoloSessionCreate,db:AsyncSession = Depends(get_session)):
    user = await db.get(models.User, session.user_id)
    if not user:
        return HTTPException(status_code=404, detail=f'user with id:{session.user_id} not found')
    book = await db.get(models.Book, session.book_id)
    if not book:
        return HTTPException(status_code=404, detail=f'book with id:{session.book_id} not found')

    db_session = models.Solo_Session(        
        book_id = session.book_id,
        user_id= session.user_id
    )
    db.add(db_session)
    try:
        await db.commit()
        await db.refresh(db_session)
    except:
        await db.rollback()
        return HTTPException(status_code=400, detail="failed to create session")
    return db_session

async def get_solo_session(
        user_id:int = Query(None),
        book_id:int = Query(None),
        db:AsyncSession = Depends(get_session)):
    if user_id is None and book_id is None:
        raise HTTPException(
            status_code=400,
            detail="Хотя бы один из query параметров не должен быть None"
        )
    elif user_id is not None and book_id is None:
        q = select(models.Solo_Session).where(models.Solo_Session.user_id == user_id)
        result = (await db.execute(q)).scalars().all()
        return result
    elif user_id is not None and book_id is not None:
        q = select(models.Solo_Session).where(models.Solo_Session.user_id == user_id).where(models.Solo_Session.book_id == book_id)
        result = (await db.execute(q)).scalar_one_or_none()
        return result
