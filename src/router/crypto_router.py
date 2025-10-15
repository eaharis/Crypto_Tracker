# router/crypto_router.py

from fastapi import APIRouter
from src.services.data_service import crypto_cache, get_top_50
from fastapi import FastAPI
from fastapi.responses import FileResponse

crypto_router = APIRouter()

@crypto_router.get("/cryptos")
def get_cryptos():
    """
    Returns the top 50 cryptos by market cap from the in-memory cache.
    """
    return {
        "last_update": crypto_cache["last_update"],
        "cryptos": get_top_50()
    }

@crypto_router.get("/cryptos/all")
def get_all_cryptos():
    """
    Returns the entire in-memory list of all cryptos (which could be thousands).
    """
    return {
        "last_update": crypto_cache["last_update"],
        "count": len(crypto_cache["data"]),
        "cryptos": crypto_cache["data"]
    }

@crypto_router.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")
