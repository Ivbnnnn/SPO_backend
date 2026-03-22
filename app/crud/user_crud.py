# app/crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import models, schemas
from sqlalchemy import select, func, cast, Float, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, Depends
from deps import get_session
from passlib.context import CryptContext
# USER
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


async def create_user(user:schemas.UserCreate,db:AsyncSession = Depends(get_session)):
    db_user = models.User(
        name=user.name,
        last_name = user.last_name,
        password=hash_password(user.password),
        email = user.email
    )
    db.add(db_user)
    try:
        await db.commit()
        await db.refresh(db_user)
    except:
        await db.rollback()
        return HTTPException(status_code=400, detail="Error")
    return db_user


async def read_user(user:schemas.UserRead,db:AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(models.User).where(models.User.id == user.id)
    )
    return result.scalar_one_or_none()


async def update_user(user:schemas.UserUpdate,db:AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(models.User).where(models.User.id == user.id)
    )
    db_user = result.scalar_one_or_none()
    db_user.name = user.name
    db_user.last_name = user.last_name
    db_user.password = hash_password(user.password)
    db_user.email = user.email
    try:
        await db.commit()
        await db.refresh(db_user)
    except:
        await db.rollback()
        return HTTPException(status_code=400, detail="Error")
    
    return db_user


async def delete_user(user:schemas.UserCreate,db:AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(models.User).where(models.User.id == user.id)
    )
    db_user = result.scalar_one_or_none()
    db.delete(db_user)
    try:
        await db.commit()
    except:
        await db.rollback()
        return HTTPException(status_code=400, detail="Error")
    return db_user