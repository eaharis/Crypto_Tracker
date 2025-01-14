# router/crypto_router.py
from fastapi import APIRouter
from services.data_service import crypto_cache

crypto_router = APIRouter()

@crypto_router.get("/cryptos")
def get_cryptos():
    """
    Returns the top 50 cryptos from the in-memory cache.
    """
    return {
        "last_update": crypto_cache["last_update"],
        "cryptos": crypto_cache["data"]
    }