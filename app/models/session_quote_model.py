# app/models.py
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Text, UniqueConstraint, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from typing import Optional, List



class Session_Quote(Base):
    __tablename__ = "session_quote"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    selected_text:Mapped[str] = mapped_column(Text, nullable=False)
    color:Mapped[str] = mapped_column(String(50), nullable=False)
    session_id: Mapped[bool] = mapped_column (ForeignKey('session.id'), nullable=False)
    
    