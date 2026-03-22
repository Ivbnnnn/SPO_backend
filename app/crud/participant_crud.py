from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import models, schemas
from sqlalchemy import select, func, cast, Float, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, Depends, Form, File, UploadFile
from deps import get_session
from minio_api import upload_cover_to_minio, delete_book_from_minio, upload_book_to_minio
from typing import Optional


async def create_participant( 
    user_id:int,
    session_id:int,
    db:AsyncSession = Depends(get_session)
    ):
    user = await db.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session = await db.get(models.Session, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    db_participant = models.Session_Participant(user_id = user_id, session_id = session_id, role_id = 2)
    db.add(db_participant)
    try:
        await db.commit()
        await db.refresh(db_participant)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    return db_participant

async def join_participant( 
    participant: schemas.ParticipantCreate,
    db:AsyncSession = Depends(get_session)
    ):
    user = await db.get(models.User, participant.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session = await db.get(models.Session, participant.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    db_participant = models.Session_Participant(user_id = participant.user_id, session_id = participant.session_id, role_id = 1)
    db.add(db_participant)
    try:
        await db.commit()
        await db.refresh(db_participant)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    return db_participant