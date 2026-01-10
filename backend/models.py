"""
Database models for the application
"""
from sqlalchemy import Column, Integer, String
from database import Base

class Player(Base):
    """
    Player model representing a sports player
    """
    __tablename__ = "players"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Player information
    name = Column(String(100), nullable=False)
    team = Column(String(100), nullable=False)
    nationality = Column(String(100), nullable=True)
    position = Column(String(50), nullable=True)
    
    def __repr__(self):
        return f"<Player(name={self.name}, team={self.team})>"
