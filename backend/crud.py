"""
CRUD operations for database interactions
"""
from sqlalchemy.orm import Session
from models import Player
from schemas import PlayerCreate
from typing import List

def get_all_players(db: Session) -> List[Player]:
    """
    Retrieve all players from the database
    
    Args:
        db: Database session
    
    Returns:
        List of all players
    """
    return db.query(Player).all()

def create_player(db: Session, player: PlayerCreate) -> Player:
    """
    Create a new player in the database
    
    Args:
        db: Database session
        player: Player data to create
    
    Returns:
        Created player object
    """
    db_player = Player(
        name=player.name,
        team=player.team,
        nationality=player.nationality,
        position=player.position
    )
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

def player_exists(db: Session, name: str, team: str) -> bool:
    """
    Check if a player already exists in the database
    
    Args:
        db: Database session
        name: Player name
        team: Player team
    
    Returns:
        True if player exists, False otherwise
    """
    return db.query(Player).filter(
        Player.name == name,
        Player.team == team
    ).first() is not None

def clear_all_players(db: Session):
    """
    Delete all players from the database (for testing purposes)
    
    Args:
        db: Database session
    """
    db.query(Player).delete()
    db.commit()
