# app/crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import models, schemas
from sqlalchemy import select, func, cast, Float, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, Depends, Form, File, UploadFile
from deps import get_session
from minio_api import upload_item_to_minio, delete_item_from_minio
from typing import Optional
# ITEM

async def create_item( 
    item_name:str = Form(...),
    item_description:str = Form(...),
    owner_id:int = Form(...),
    file:UploadFile = File(...),  db:AsyncSession = Depends(get_session)
    ):

    user = await db.get(models.User, owner_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    item_src =await upload_item_to_minio(file) 
    db_item = models.Item(item_name=item_name, description=item_description, src=item_src, owner=user)
    db.add(db_item)
    try:
        await db.commit()
        await db.refresh(db_item)        
    except:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Error")

#Itemview
async def read_item_by_id(item_id:int,db:AsyncSession = Depends(get_session)):
    q = select(models.Item).where(models.Item.item_id == item_id)
    item = (await db.execute(q)).scalar_one_or_none()
    if (not item):
        return HTTPException(status_code=400, detail="Error")
    return item

#UserPage
async def read_item_by_owner(user_id:int,db:AsyncSession = Depends(get_session)):
    q = select(models.Item).where(models.Item.owner_id == user_id)
    items = (await db.execute(q)).scalars().all()
    if (not items):
        return HTTPException(status_code=400, detail="Error")
    return items

#future crud for reccomendations for HomePage
async def read_items(db: AsyncSession = Depends(get_session)):
    q = select(models.Item).order_by(models.Item.item_id.desc()).limit(5)
    items = (await db.execute(q)).scalars().all()
    return items

# надо выключать при запросе file если не обновляем картинку
async def update_item( 
    item_id:int = Form(...),
    item_name:Optional[str] = Form(...),
    item_description:Optional[str] = Form(...),
    file:Optional[UploadFile] = File(...),
    db:AsyncSession = Depends(get_session)
):
    q = select(models.Item).where(models.Item.item_id == item_id)
    item = (await (db.execute(q))).scalar_one_or_none()

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    if item_name:
        item.item_name = item_name
    if item_description:
        item.description = item_description
    if file:
        src = item.src
        if src:
            await delete_item_from_minio(src)

        item.src = await upload_item_to_minio(file=file)

    try:
        await db.commit()
        await db.refresh(item)
    except:
        await db.rollback()
        return HTTPException(status_code=400, detail="Error")
    return item


async def delete_item(item_id: int, db: AsyncSession):
    q = select(models.Item).where(models.Item.item_id == item_id)
    item = (await db.execute(q)).scalar_one_or_none()
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    old_src = item.src
    try:
        await db.delete(item)
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Error deleting item from DB")

    if old_src:
        try:
            await delete_item_from_minio(old_src)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Item deleted from DB, but failed to delete file: {e}")

    return {"message": "success"}