# app/models.py
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Text, UniqueConstraint, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from typing import Optional, List
from .session_participant_model import Session_Participant
from .session_note_model import Session_Note
from .session_quote_model import Session_Quote
class Session(Base):
    __tablename__ = "sessions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column (String(50), nullable=False)
    book_id: Mapped[int] = mapped_column (ForeignKey('books.id'), nullable=False)
    is_active: Mapped[bool] = mapped_column (Boolean, nullable=False)
    user_id: Mapped[int] = mapped_column (ForeignKey('users.id'), nullable=False)

    participants: Mapped[List["Session_Participant"]] = relationship("Session_Participant", back_populates='session_id', cascade="all, delete-orphan")
    session_notes: Mapped[List["Session_Note"]] = relationship("Session_Note", back_populates='session_id', cascade="all, delete-orphan")
    session_quotes: Mapped[List["Session_Quote"]] = relationship("Session_Quote", back_populates='session_id', cascade="all, delete-orphan")