from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime
from typing import List
from datetime import datetime
from app.models.base import Base, TimestampUUIDMixin

class Tournament(Base, TimestampUUIDMixin):
    __tablename__ = "tournaments"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    max_players: Mapped[int] = mapped_column(Integer, nullable=False)
    start_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    players: Mapped[List["Player"]] = relationship("Player", back_populates="tournament", cascade="all, delete-orphan")
