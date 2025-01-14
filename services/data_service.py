# services/data_service.py
from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from db.models import CryptoEntry
from db.session import SessionLocal
from services.cmc_service import fetch_top_cryptos

# In-memory cache
crypto_cache = {
    "last_update": None,
    "data": [],
}


def load_data_from_db_into_cache() -> None:
    """Load existing DB data into the in-memory cache."""
    db = SessionLocal()
    try:
        rows = db.query(CryptoEntry).order_by(CryptoEntry.cmc_rank).all()
        cryptos = []
        for row in rows:
            cryptos.append({
                "id": row.coin_id,
                "name": row.name,
                "symbol": row.symbol,
                "cmc_rank": row.cmc_rank,
                "quote": {
                    "USD": {
                        "price": row.price,
                        "volume_24h": row.volume_24h,
                        "percent_change_24h": row.percent_change_24h,
                        "market_cap": row.market_cap,
                    }
                }
            })
        crypto_cache["data"] = cryptos
        crypto_cache["last_update"] = datetime.utcnow()
        print(f"Loaded {len(cryptos)} cryptos from DB into cache.")
    finally:
        db.close()


def update_cache_and_db(limit=50) -> None:
    """Fetch top cryptos from API, update the in-memory cache, and persist in DB."""
    try:
        cryptos = fetch_top_cryptos(limit=limit)

        # Update in-memory cache
        crypto_cache["data"] = cryptos
        crypto_cache["last_update"] = datetime.utcnow()
        print(f"[{datetime.utcnow()}] Updated in-memory cache with {len(cryptos)} entries.")

        # Update DB
        db = SessionLocal()
        try:
            db.query(CryptoEntry).delete()
            for coin in cryptos:
                quote = coin.get("quote", {}).get("USD", {})
                entry = CryptoEntry(
                    coin_id=coin["id"],
                    name=coin["name"],
                    symbol=coin["symbol"],
                    cmc_rank=coin["cmc_rank"],
                    price=quote.get("price"),
                    volume_24h=quote.get("volume_24h"),
                    percent_change_24h=quote.get("percent_change_24h"),
                    market_cap=quote.get("market_cap"),
                    last_updated=datetime.utcnow()
                )
                db.add(entry)
            db.commit()
        finally:
            db.close()
    except Exception as e:
        print(f"Error in update_cache_and_db: {e}")