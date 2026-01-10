"""
Test script to verify API key and database connection
"""
import requests
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")
DATABASE_URL = os.getenv("DATABASE_URL")

print("=" * 60)
print("TESTING CONFIGURATION")
print("=" * 60)

# Test 1: Check environment variables
print("\n1. Environment Variables:")
print(f"   RAPIDAPI_KEY: {'✓ Set' if RAPIDAPI_KEY else '✗ Missing'}")
print(f"   RAPIDAPI_HOST: {'✓ Set' if RAPIDAPI_HOST else '✗ Missing'}")
print(f"   DATABASE_URL: {'✓ Set' if DATABASE_URL else '✗ Missing'}")

if RAPIDAPI_KEY:
    print(f"   API Key (first 10 chars): {RAPIDAPI_KEY[:10]}...")

# Test 2: Test Database Connection
print("\n2. Testing Database Connection:")
try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("   ✓ Database connection successful!")
        
        # Check if players table exists
        result = conn.execute(text("SHOW TABLES LIKE 'players'"))
        if result.fetchone():
            print("   ✓ 'players' table exists")
            
            # Count players
            result = conn.execute(text("SELECT COUNT(*) FROM players"))
            count = result.fetchone()[0]
            print(f"   ✓ Current player count: {count}")
        else:
            print("   ✗ 'players' table not found")
except Exception as e:
    print(f"   ✗ Database connection failed: {e}")

# Test 3: Test RapidAPI Connection
print("\n3. Testing RapidAPI Connection:")

# Try the fixtures endpoint from user's example
print("\n   A) Testing fixtures/headtohead endpoint:")
try:
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/headtohead"
    querystring = {"h2h": "33-34"}
    headers = {
        "x-rapidapi-host": RAPIDAPI_HOST,
        "x-rapidapi-key": RAPIDAPI_KEY
    }
    
    response = requests.get(url, headers=headers, params=querystring, timeout=10)
    print(f"   Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ API call successful!")
        print(f"   Response keys: {list(data.keys())}")
        if "response" in data:
            print(f"   Number of results: {len(data['response'])}")
    elif response.status_code == 403:
        print(f"   ✗ 403 Forbidden - Authentication issue")
        print(f"   Response: {response.text[:300]}")
    else:
        print(f"   ✗ Error: {response.status_code}")
        print(f"   Response: {response.text[:300]}")
except Exception as e:
    print(f"   ✗ Request failed: {e}")

# Try teams endpoint
print("\n   B) Testing teams endpoint:")
try:
    url = "https://api-football-v1.p.rapidapi.com/v3/teams"
    querystring = {"id": "33"}  # Manchester United
    headers = {
        "x-rapidapi-host": RAPIDAPI_HOST,
        "x-rapidapi-key": RAPIDAPI_KEY
    }
    
    response = requests.get(url, headers=headers, params=querystring, timeout=10)
    print(f"   Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ API call successful!")
        print(f"   Response keys: {list(data.keys())}")
        if "response" in data:
            print(f"   Number of results: {len(data['response'])}")
    elif response.status_code == 403:
        print(f"   ✗ 403 Forbidden - Authentication issue")
        print(f"   Response: {response.text[:300]}")
    else:
        print(f"   ✗ Error: {response.status_code}")
        print(f"   Response: {response.text[:300]}")
except Exception as e:
    print(f"   ✗ Request failed: {e}")

# Try status endpoint (usually free)
print("\n   C) Testing status endpoint (free):")
try:
    url = "https://api-football-v1.p.rapidapi.com/v3/status"
    headers = {
        "x-rapidapi-host": RAPIDAPI_HOST,
        "x-rapidapi-key": RAPIDAPI_KEY
    }
    
    response = requests.get(url, headers=headers, timeout=10)
    print(f"   Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ API authentication works!")
        print(f"   Response: {data}")
    elif response.status_code == 403:
        print(f"   ✗ 403 Forbidden - API Key might be invalid or expired")
        print(f"   Response: {response.text[:300]}")
    else:
        print(f"   ✗ Error: {response.status_code}")
        print(f"   Response: {response.text[:300]}")
except Exception as e:
    print(f"   ✗ Request failed: {e}")

print("\n" + "=" * 60)
print("DIAGNOSIS COMPLETE")
print("=" * 60)
