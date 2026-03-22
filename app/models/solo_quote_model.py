# app/models.py
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from typing import Optional, List

class Solo_Quote(Base):
    __tablename__ = "solo_quote"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    selected_text:Mapped[str] = mapped_column(Text, nullable=False)
    color:Mapped[str] = mapped_column(String(50), nullable=False)
    solo_session_id:Mapped[str] = mapped_column(ForeignKey('solo_sessions.id'), nullable=False)
