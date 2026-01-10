"""
Pydantic schemas for request and response validation
"""
from pydantic import BaseModel
from typing import Optional

class PlayerBase(BaseModel):
    """
    Base schema for player data
    """
    name: str
    team: str
    nationality: Optional[str] = None
    position: Optional[str] = None

class PlayerCreate(PlayerBase):
    """
    Schema for creating a new player
    """
    pass

class PlayerResponse(PlayerBase):
    """
    Schema for player response (includes id)
    """
    id: int
    
    class Config:
        from_attributes = True  # Updated from orm_mode for Pydantic v2
