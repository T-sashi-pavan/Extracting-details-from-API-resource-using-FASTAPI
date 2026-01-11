# API Data Extraction with FastAPI

Simple project to extract and manage data using FastAPI backend and React frontend.

## Setup

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python main.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## What it does

- FastAPI handles the API endpoints
- React frontend for interacting with the API
- SQLite database for storing data

Backend runs on `http://localhost:8000`  
Frontend runs on `http://localhost:5173`

## Files

- `backend/main.py` - API routes
- `backend/models.py` - Database models
- `backend/crud.py` - Database operations
- `frontend/src/App.jsx` - Main React component

That's it. Pretty straightforward.
