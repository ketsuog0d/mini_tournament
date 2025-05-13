from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists
from sqlalchemy.exc import IntegrityError
from typing import List
from uuid import UUID
from app.models.player import Player

class PlayerRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def register_player(self, name: str, email: str, tournament_id: UUID) -> Player:
        player = Player(name=name, email=email, tournament_id=tournament_id)
        self.session.add(player)
        try:
            await self.session.flush()
        except IntegrityError:
            await self.session.rollback()
            raise ValueError("Email already registered for this tournament")
        return player

    async def is_email_registered(self, tournament_id: UUID, email: str) -> bool:
        result = await self.session.execute(
            select(exists().where(
                (Player.tournament_id == tournament_id) &
                (Player.email == email)
            ))
        )
        return result.scalar()

    async def get_players_by_tournament(self, tournament_id: UUID) -> List[Player]:
        result = await self.session.execute(
            select(Player).where(Player.tournament_id == tournament_id)
        )
        return result.scalars().all()
