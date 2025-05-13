from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.schemas.tournament import (
    TournamentCreate, TournamentRead,
    PlayerRegister, PlayerRead
)
from app.services.tournament import TournamentService
from app.db import get_session
from sqlalchemy.exc import SQLAlchemyError
from typing import List

router = APIRouter(prefix="/tournaments", tags=["Tournaments"])

def get_service(session: AsyncSession = Depends(get_session)) -> TournamentService:
    return TournamentService(session)

@router.post(
    "",
    response_model=TournamentRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new tournament",
    description="Creates a new tournament with the specified name, maximum number of players, and start time."
)
async def create_tournament(
    data: TournamentCreate,
    service: TournamentService = Depends(get_service)
):
    """
    Create a new tournament with the following parameters:
    - **name**: Tournament name (3-100 characters)
    - **max_players**: Maximum number of players (2-100)
    - **start_at**: Tournament start time (must be in the future)
    """
    try:
        tournament = await service.create_tournament(**data.dict())
        return TournamentRead(
            id=tournament.id,
            name=tournament.name,
            max_players=tournament.max_players,
            start_at=tournament.start_at,
            registered_players=len(tournament.players)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred while creating tournament"
        )

@router.post(
    "/{tournament_id}/register",
    response_model=PlayerRead,
    summary="Register a player for a tournament",
    description="Register a new player for the specified tournament."
)
async def register_player(
    tournament_id: UUID,
    player_data: PlayerRegister,
    service: TournamentService = Depends(get_service)
):
    """
    Register a player for a tournament:
    - **tournament_id**: UUID of the tournament
    - **name**: Player's full name (2-100 characters)
    - **email**: Valid email address (must be unique per tournament)
    """
    try:
        player = await service.register_player(
            tournament_id,
            player_data.name,
            player_data.email
        )
        return player
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred while registering player"
        )

@router.get(
    "/{tournament_id}/players",
    response_model=List[PlayerRead],
    summary="Get tournament players",
    description="Retrieve a list of all players registered for the specified tournament."
)
async def get_players(
    tournament_id: UUID,
    service: TournamentService = Depends(get_service)
):
    """
    Get all players registered for a tournament:
    - **tournament_id**: UUID of the tournament
    """
    try:
        return await service.list_players(tournament_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred while retrieving players"
        )
