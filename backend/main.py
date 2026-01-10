"""
FastAPI main application
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import requests
import os
from dotenv import load_dotenv

# Import local modules
from database import engine, get_db, Base
from models import Player
from schemas import PlayerResponse, PlayerCreate
import crud

# Load environment variables
load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Sports Players API", version="1.0.0")

# Configure CORS (allow frontend to communicate with backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# API configuration
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")


@app.get("/")
def root():
    """
    Root endpoint - API health check
    """
    return {
        "message": "Sports Players API is running!",
        "endpoints": {
            "/fetch-players": "Fetch players from external API and store in DB",
            "/players": "Get all players from database"
        }
    }


@app.get("/fetch-players")
def fetch_players(db: Session = Depends(get_db)):
    """
    Fetch players data and store in database
    
    Uses Cricket API (Cricbuzz) to fetch real cricket players data.
    Falls back to demo data if API fails.
    """
    try:
        # Try to fetch from Cricket API
        url = "https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/40381/hscard"
        
        headers = {
            "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com",
            "x-rapidapi-key": RAPIDAPI_KEY
        }
        
        print(f"Making API request to: {url}")
        response = requests.get(url, headers=headers, timeout=15)
        print(f"API Response Status: {response.status_code}")
        
        players_added = 0
        
        # If API call is successful, parse cricket data
        if response.status_code == 200:
            data = response.json()
            print(f"API Response keys: {list(data.keys())}")
            
            # Check if scorecard data exists
            if "scorecard" in data and data["scorecard"]:
                # Extract batsmen from all innings
                for innings in data["scorecard"]:
                    if "batsman" in innings:
                        for batsman in innings["batsman"][:10]:  # Limit to 10 per innings
                            try:
                                player_name = batsman.get("name", "Unknown")
                                runs = batsman.get("runs", 0)
                                balls = batsman.get("balls", 0)
                                
                                # Determine team based on innings
                                team_name = "Team A" if innings.get("inningsid") == 1 else "Team B"
                                
                                # Get nationality and position
                                nationality = "Unknown"
                                position = "Batsman" if "batsman" in str(innings) else "Player"
                                
                                # Check if player already exists
                                if player_name and player_name != "Unknown":
                                    if not crud.player_exists(db, player_name, team_name):
                                        player_data = PlayerCreate(
                                            name=player_name,
                                            team=team_name,
                                            nationality=nationality,
                                            position=position
                                        )
                                        crud.create_player(db, player_data)
                                        players_added += 1
                            except Exception as e:
                                print(f"Error processing batsman: {e}")
                                continue
                
                if players_added > 0:
                    return {
                        "message": "Players fetched successfully from Cricket API",
                        "players_added": players_added,
                        "total_players_in_db": len(crud.get_all_players(db))
                    }
        
        # If API failed or no data, use demo data
        print("Using demo player data...")
        demo_players = [
            {"name": "Virat Kohli", "team": "India", "nationality": "India", "position": "Batsman"},
            {"name": "Rohit Sharma", "team": "India", "nationality": "India", "position": "Batsman"},
            {"name": "Jasprit Bumrah", "team": "India", "nationality": "India", "position": "Bowler"},
            {"name": "KL Rahul", "team": "India", "nationality": "India", "position": "Wicketkeeper"},
            {"name": "Steve Smith", "team": "Australia", "nationality": "Australia", "position": "Batsman"},
            {"name": "David Warner", "team": "Australia", "nationality": "Australia", "position": "Batsman"},
            {"name": "Pat Cummins", "team": "Australia", "nationality": "Australia", "position": "Bowler"},
            {"name": "Joe Root", "team": "England", "nationality": "England", "position": "Batsman"},
            {"name": "Ben Stokes", "team": "England", "nationality": "England", "position": "All-rounder"},
            {"name": "James Anderson", "team": "England", "nationality": "England", "position": "Bowler"},
            {"name": "Kane Williamson", "team": "New Zealand", "nationality": "New Zealand", "position": "Batsman"},
            {"name": "Trent Boult", "team": "New Zealand", "nationality": "New Zealand", "position": "Bowler"},
            {"name": "Babar Azam", "team": "Pakistan", "nationality": "Pakistan", "position": "Batsman"},
            {"name": "Shaheen Afridi", "team": "Pakistan", "nationality": "Pakistan", "position": "Bowler"},
            {"name": "Kagiso Rabada", "team": "South Africa", "nationality": "South Africa", "position": "Bowler"},
            {"name": "Quinton de Kock", "team": "South Africa", "nationality": "South Africa", "position": "Wicketkeeper"},
            {"name": "Rashid Khan", "team": "Afghanistan", "nationality": "Afghanistan", "position": "Bowler"},
            {"name": "AB de Villiers", "team": "South Africa", "nationality": "South Africa", "position": "Batsman"},
            {"name": "Chris Gayle", "team": "West Indies", "nationality": "West Indies", "position": "Batsman"},
            {"name": "Shakib Al Hasan", "team": "Bangladesh", "nationality": "Bangladesh", "position": "All-rounder"},
        ]
        
        for player_data in demo_players:
            if not crud.player_exists(db, player_data["name"], player_data["team"]):
                player = PlayerCreate(
                    name=player_data["name"],
                    team=player_data["team"],
                    nationality=player_data["nationality"],
                    position=player_data["position"]
                )
                crud.create_player(db, player)
                players_added += 1
        
        return {
            "message": "Players fetched successfully (demo data)",
            "players_added": players_added,
            "total_players_in_db": len(crud.get_all_players(db))
        }
    
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/players", response_model=List[PlayerResponse])
def get_players(db: Session = Depends(get_db)):
    """
    Get all players from the database
    
    Returns:
        List of all players stored in the database
    """
    try:
        players = crud.get_all_players(db)
        return players
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.delete("/players")
def delete_all_players(db: Session = Depends(get_db)):
    """
    Delete all players from database (for testing purposes)
    """
    try:
        crud.clear_all_players(db)
        return {"message": "All players deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
