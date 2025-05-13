from pydantic import BaseModel, EmailStr, Field, validator
from uuid import UUID
from datetime import datetime
from typing import Optional

# --- Tournament Schemas ---

class TournamentCreate(BaseModel):
    name: str = Field(
        ...,
        max_length=100,
        min_length=3,
        description="Name of the tournament"
    )
    max_players: int = Field(
        ...,
        gt=1,
        le=100,
        description="Maximum number of players allowed in the tournament"
    )
    start_at: datetime = Field(
        ...,
        description="Tournament start date and time"
    )

    @validator('start_at')
    def validate_start_time(cls, v):
        if v <= datetime.now():
            raise ValueError("Tournament start time must be in the future")
        return v

class TournamentRead(BaseModel):
    id: UUID
    name: str
    max_players: int
    start_at: datetime
    registered_players: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Summer Chess Tournament",
                "max_players": 32,
                "start_at": "2024-06-01T10:00:00Z",
                "registered_players": 0
            }
        }


# --- Player Schemas ---

class PlayerRegister(BaseModel):
    name: str = Field(
        ...,
        max_length=100,
        min_length=2,
        description="Player's full name"
    )
    email: EmailStr = Field(
        ...,
        description="Player's email address for tournament communications"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Daniil Krishkovec",
                "email": "spiritdonk@example.com"
            }
        }

class PlayerRead(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    tournament_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Daniil Krishkovec",
                "email": "spiritdonk@example.com",
                "tournament_id": "123e4567-e89b-12d3-a456-426614174000",
                "created_at": "2024-03-15T10:00:00Z"
            }
        }
