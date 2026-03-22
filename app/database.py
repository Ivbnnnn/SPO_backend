# app/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")

# async engine (пул внутри asyncpg)
engine = create_async_engine(DATABASE_URL, future=True, echo=False, pool_size=10, max_overflow=20)

# factory for AsyncSession
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    future=True,
)

Base = declarative_base()

# helper to create tables in dev (run at startup or вручную)
async def init_models():
    async with engine.begin() as conn:
        # run_sync выполнит синхронную функцию (metadata.create_all) в контексте соединения
        await conn.run_sync(Base.metadata.create_all)

