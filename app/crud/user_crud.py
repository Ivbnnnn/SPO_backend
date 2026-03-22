# app/crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import models, schemas
from sqlalchemy import select, func, cast, Float, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, Depends
from deps import get_session
# USER

async def create_user(user:schemas.UserCreate,db:AsyncSession = Depends(get_session)):
    db_user = models.User(user_name=user.user_name, age=user.age, user_password=user.user_password)
    db.add(db_user)
    try:
        await db.commit()
        await db.refresh(db_user)
    except:
        await db.rollback()
        return HTTPException(status_code=400, detail="Error")
    return db_user


async def read_user(user:schemas.UserCreate,db:AsyncSession = Depends(get_session)):
    db_user = models.User(user_name=user.user_name, age=user.age, user_password=user.user_password)
    db.add(db_user)
    try:
        await db.commit()
        await db.refresh(db_user)
    except:
        await db.rollback()
        return HTTPException(status_code=400, detail="Error")
    return db_user


async def update_user(user:schemas.UserCreate,db:AsyncSession = Depends(get_session)):
    db_user = models.User(user_name=user.user_name, age=user.age, user_password=user.user_password)
    db.add(db_user)
    try:
        await db.commit()
        await db.refresh(db_user)
    except:
        await db.rollback()
        return HTTPException(status_code=400, detail="Error")
    return db_user


async def delete_user(user:schemas.UserCreate,db:AsyncSession = Depends(get_session)):
    db_user = models.User(user_name=user.user_name, age=user.age, user_password=user.user_password)
    db.add(db_user)
    try:
        await db.commit()
        await db.refresh(db_user)
    except:
        await db.rollback()
        return HTTPException(status_code=400, detail="Error")
    return db_user