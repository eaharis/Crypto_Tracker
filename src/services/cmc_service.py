# services/cmc_service.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("COINMARKETCAP_API_KEY")
BASE_URL = "https://pro-api.coinmarketcap.com/v1"
LIMIT = 200

if not API_KEY:
    raise ValueError("CoinMarketCap API key not found. Please set COINMARKETCAP_API_KEY in .env")

def fetch_all_cryptos():
    """
    Fetch as many cryptos as possible from CoinMarketCap.
    The 'limit' can be set very high (e.g., 10000) to attempt to retrieve all coins.
    """
    url = f"{BASE_URL}/cryptocurrency/listings/latest"
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": API_KEY,
    }
    params = {
        "start": 1,
        "limit": LIMIT,
        "convert": "USD",
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("data", [])