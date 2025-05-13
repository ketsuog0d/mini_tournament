from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from uuid import UUID
from app.models.base import Base, TimestampUUIDMixin
from sqlalchemy import UniqueConstraint

class Player(Base, TimestampUUIDMixin):
    __tablename__ = "players"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)

    tournament_id: Mapped[UUID] = mapped_column(ForeignKey("tournaments.id", ondelete="CASCADE"))
    tournament: Mapped["Tournament"] = relationship("Tournament", back_populates="players")

    __table_args__ = (
        UniqueConstraint("email", "tournament_id", name="uq_email_tournament"),
        {"sqlite_autoincrement": True},
    )
