from uuid import UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.tournament import TournamentRepository
from app.repositories.player import PlayerRepository
from app.models.tournament import Tournament
from app.models.player import Player
from typing import List

class TournamentService:
    def __init__(self, session: AsyncSession):
        self.tournament_repo = TournamentRepository(session)
        self.player_repo = PlayerRepository(session)

    async def create_tournament(self, name: str, max_players: int, start_at: datetime) -> Tournament:
        """
        Create a new tournament.
        
        Args:
            name: Tournament name (3-100 characters)
            max_players: Maximum number of players allowed (2-100)
            start_at: Tournament start time (must be in the future)
            
        Returns:
            Tournament: Created tournament instance
            
        Raises:
            ValueError: If validation fails
        """
        # Additional validation
        if start_at <= datetime.now():
            raise ValueError("Tournament start time must be in the future")
        
        if len(name.strip()) < 3:
            raise ValueError("Tournament name must be at least 3 characters long")
            
        if max_players < 2:
            raise ValueError("Tournament must allow at least 2 players")
        elif max_players > 100:
            raise ValueError("Tournament cannot have more than 100 players")

        return await self.tournament_repo.create_tournament(name.strip(), max_players, start_at)

    async def register_player(self, tournament_id: UUID, name: str, email: str) -> Player:
        """
        Register a player for a tournament.
        
        Args:
            tournament_id: UUID of the tournament
            name: Player's full name (2-100 characters)
            email: Valid email address
            
        Returns:
            Player: Registered player instance
            
        Raises:
            ValueError: If validation fails or tournament is full
        """
        # Validate player name
        name = name.strip()
        if len(name) < 2:
            raise ValueError("Player name must be at least 2 characters long")
        elif len(name) > 100:
            raise ValueError("Player name cannot exceed 100 characters")

        # Get tournament and validate
        tournament = await self.tournament_repo.get_by_id(tournament_id)
        if not tournament:
            raise ValueError("Tournament not found")

        # Check if tournament has started
        if tournament.start_at <= datetime.now():
            raise ValueError("Cannot register for a tournament that has already started")

        # Check for duplicate registration
        if await self.player_repo.is_email_registered(tournament_id, email):
            raise ValueError("A player with this email is already registered for this tournament")

        # Check tournament capacity
        current_count = await self.tournament_repo.get_players_count(tournament_id)
        if current_count >= tournament.max_players:
            raise ValueError("Tournament is full")

        return await self.player_repo.register_player(name, email.lower(), tournament_id)

    async def list_players(self, tournament_id: UUID) -> List[Player]:
        """
        Get all players registered for a tournament.
        
        Args:
            tournament_id: UUID of the tournament
            
        Returns:
            List[Player]: List of registered players
            
        Raises:
            ValueError: If tournament not found
        """
        # Verify tournament exists
        tournament = await self.tournament_repo.get_by_id(tournament_id)
        if not tournament:
            raise ValueError("Tournament not found")
            
        return await self.player_repo.get_players_by_tournament(tournament_id)
