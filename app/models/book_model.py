# app/models.py
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from typing import Optional, List

class Book(Base):
    __tablename__ = "book"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    title: Mapped[str] = mapped_column (String(50), nullable=False)
    author: Mapped[str] = mapped_column (String(50), nullable=False)
    content_path: Mapped[str] = mapped_column (String(50), nullable=False)
    cover_img: Mapped[str] = mapped_column (String(50), nullable=False)
    