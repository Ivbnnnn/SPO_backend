from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import models, schemas
from sqlalchemy import select, func, cast, Float, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, Depends
from deps import get_session
from passlib.context import CryptContext
import uuid

# Session

async def create_session(session:schemas.SessionCreate,user_id:int,db:AsyncSession = Depends(get_session)):
    user = await db.get(models.User, user_id)
    if not user:
        return HTTPException(status_code=404, detail=f'user with id:{user_id} not found')
    book = await db.get(models.Book, session.book_id)
    if not book:
        return HTTPException(status_code=404, detail=f'book with id:{session.book_id} not found')

    db_session = models.Session(
        name=session.name,
        book_id = session.book_id,
        user_id= user_id,
        link=uuid.uuid4().hex 
    )
    db.add(db_session)
    try:
        await db.commit()
        await db.refresh(db_session)
    except:
        await db.rollback()
        return HTTPException(status_code=400, detail="failed to create session")
    return db_session


async def get_participants_by_session_id(session_id:int,db:AsyncSession = Depends(get_session)):
    session = await db.get(models.Session, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session  not found")
    participants = session.participants 
    return participants


async def get_session_by_link(link:str,db:AsyncSession = Depends(get_session)):
    q = select(models.Session).where(models.Session.link == link)
    session = (await db.execute(q)).scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Session  not found")
    return session
