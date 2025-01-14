# main.py
import os
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

load_dotenv()

API_KEY = os.environ.get("COINMARKETCAP_API_KEY")
BASE_URL = "https://pro-api.coinmarketcap.com/v1"

if not API_KEY:
    raise ValueError("CoinMarketCap API key not found. Please set COINMARKETCAP_API_KEY in .env")

app = FastAPI()

# Enable CORS so React can call this API from http://localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify ["http://localhost:3000"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory cache for the top 50 cryptos
crypto_cache = {
    "last_update": None,
    "data": [],
}

def fetch_top_cryptos(limit=50):
    """Fetch top N cryptos by market cap from CoinMarketCap API."""
    url = f"{BASE_URL}/cryptocurrency/listings/latest"
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": API_KEY,
    }
    params = {
        "start": 1,
        "limit": limit,
        "convert": "USD",
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("data", [])

def update_crypto_cache():
    """Scheduler job: refresh the crypto_cache data every 15 minutes."""
    try:
        cryptos = fetch_top_cryptos(limit=50)
        # Store in global cache
        crypto_cache["data"] = cryptos
        crypto_cache["last_update"] = datetime.utcnow()
        print(f"[{datetime.utcnow()}] Crypto cache updated. Count: {len(cryptos)}")
    except Exception as e:
        # If there's an issue fetching data, log it but keep old data
        print(f"Error updating crypto cache: {e}")

# Schedule the update job to run every 15 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(update_crypto_cache, "interval", minutes=15)
scheduler.start()

# Run once on startup so we have initial data
@app.on_event("startup")
def startup_event():
    update_crypto_cache()

@app.get("/")
def read_root():
    return {"message": "CoinMarketCap Integration with Cache is Running"}

@app.get("/cryptos")
def get_cryptos():
    """
    Returns the cached list of top 50 cryptos.
    The front end will sort/filter as needed.
    """
    return {
        "last_update": crypto_cache["last_update"],
        "cryptos": crypto_cache["data"]
    }

# Graceful shutdown for the scheduler
@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()