from fastapi import FastAPI
from fastapi import Depends
import minio_api 
from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import models, crud
import schemas
from database import engine, Base, init_models
from deps import get_session
import asyncio
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()



# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# app.include_router(minio_api.router)


@app.on_event("startup")
async def on_startup():
    """
    Попытки подключиться к БД и инициализировать модели (create_all) с ретраями.
    Если БД не готова сразу (например, при поднятии контейнеров), код будет ждать.
    """
    max_retries = 10        # сколько раз пробуем
    delay = 1.0             # начальная задержка в секундах
    max_delay = 10.0        # максимальная задержка
    for attempt in range(1, max_retries + 1):
        try:
            await init_models()
            break
        except Exception as e:
            if attempt == max_retries:
                # Если последний попытка — пробрасываем исключение, чтобы приложение упало и лог показал причину.
                raise
            # Ждём перед следующей попыткой (экспоненциальный бэкофф)
            await asyncio.sleep(delay)
            delay = min(delay * 2, max_delay)

@app.post('/add_user', response_model=schemas.UserCreate, tags=["User"])
async def add_user(user:schemas.UserCreate,db:AsyncSession = Depends(get_session)):
    return await crud.create_user(user, db)

# @app.post('/add_item', tags=["Item"])
# async def add_item( 
#     item_name:str = Form(...),
#     item_description:str = Form(...),
#     owner_id:int = Form(...),
#     file:UploadFile = File(...),
#     db:AsyncSession = Depends(get_session)
#     ):
#     return await crud.create_item(item_name=item_name, item_description=item_description, owner_id=owner_id, file=file, db=db)

# @app.patch('/update_item',  tags=["Item"], response_model=schemas.item_schema.ItemRead)
# async def update_item( 
#     item_id:int = Form(...),
#     item_name:Optional[str] = Form(None),
#     item_description:Optional[str] = Form(None),
#     file:Optional[UploadFile] = File(None),
#     db:AsyncSession = Depends(get_session)):
#     return await crud.update_item(item_id=item_id, item_name=item_name, item_description=item_description, file=file, db=db)


# @app.get('/get_items/{item_id}', response_model=schemas.ItemRead, tags=["Item"])
# async def get_items(item_id:int,db:AsyncSession = Depends(get_session)):
#     return await crud.read_item_by_id(item_id, db)

# @app.get('/get_owner_items/{user_id}', response_model=list[schemas.ItemRead], tags=["Item"])
# async def get_owner_items(user_id:int,db:AsyncSession = Depends(get_session)):
#     return await crud.read_item_by_owner(user_id, db)

# @app.get("/get_items", response_model=list[schemas.ItemRead], tags=["Item"])
# async def get_items(db: AsyncSession = Depends(get_session)):
#     return await crud.read_items(db)

# @app.delete('/delete_item/{item_id}', tags=["Item"])
# async def delete_item( 
#     item_id:int,
#     db:AsyncSession = Depends(get_session)
#     ):
#     return await crud.delete_item(item_id=item_id, db=db)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000)






