from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from uuid import UUID
from typing import Optional
from app.models.tournament import Tournament
from app.models.player import Player

class TournamentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_tournament(self, name: str, max_players: int, start_at) -> Tournament:
        tournament = Tournament(name=name, max_players=max_players, start_at=start_at)
        self.session.add(tournament)
        await self.session.flush()
        return tournament

    async def get_by_id(self, tournament_id: UUID) -> Optional[Tournament]:
        result = await self.session.execute(
            select(Tournament).where(Tournament.id == tournament_id)
        )
        return result.scalar_one_or_none()

    async def get_players_count(self, tournament_id: UUID) -> int:
        result = await self.session.execute(
            select(func.count(Player.id)).where(Player.tournament_id == tournament_id)
        )
        return result.scalar_one()
