# services/data_service.py

import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from db.session import SessionLocal
from db.models import CryptoEntry
from services.cmc_service import fetch_all_cryptos

load_dotenv()

DEV_MODE = os.environ.get("DEV_MODE", "0").lower() in ("1", "true")

# In-memory cache for storing the entire list of coins
crypto_cache = {
    "last_update": None,
    "data": [],  # This will hold the entire list from the last fetch
}

def load_db_into_cache():
    """
    Load existing data from DB into the in-memory cache if dev mode is on
    (or if you want to preserve last known data on startup).
    """
    db = SessionLocal()
    try:
        rows = db.query(CryptoEntry).all()
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
        crypto_cache["last_update"] = datetime.now(tz=timezone.utc)
        print(f"[load_db_into_cache] Loaded {len(cryptos)} rows from DB.")
    finally:
        db.close()

def update_cache_and_db() -> None:
    """
    If dev mode is on, skip external API calls and just load from DB.
    Otherwise, fetch from CoinMarketCap, upsert, and update cache.
    """
    if DEV_MODE:
        print("[DEV_MODE] Skipping external API call. Loading from DB only.")
        load_db_into_cache()
        return

    try:
        cryptos = fetch_all_cryptos()
        print(f"Fetched {len(cryptos)} coins from CoinMarketCap.")

        # Update in-memory cache
        crypto_cache["data"] = cryptos
        crypto_cache["last_update"] = datetime.now(tz=timezone.utc)

        # Bulk upsert into DB
        db = SessionLocal()
        try:
            for coin in cryptos:
                quote = coin.get("quote", {}).get("USD", {})
                stmt = insert(CryptoEntry).values(
                    coin_id=coin["id"],
                    name=coin["name"],
                    symbol=coin["symbol"],
                    cmc_rank=coin["cmc_rank"],
                    price=quote.get("price"),
                    volume_24h=quote.get("volume_24h"),
                    percent_change_24h=quote.get("percent_change_24h"),
                    market_cap=quote.get("market_cap"),
                )
                # On conflict with coin_id, do update
                stmt = stmt.on_conflict_do_update(
                    index_elements=["coin_id"],  # The PK/unique column
                    set_={
                        "name": stmt.excluded.name,
                        "symbol": stmt.excluded.symbol,
                        "cmc_rank": stmt.excluded.cmc_rank,
                        "price": stmt.excluded.price,
                        "volume_24h": stmt.excluded.volume_24h,
                        "percent_change_24h": stmt.excluded.percent_change_24h,
                        "market_cap": stmt.excluded.market_cap,
                    },
                )
                db.execute(stmt)
            db.commit()
        finally:
            db.close()

        print("[update_cache_and_db] Successfully upserted data to DB.")
    except Exception as e:
        print(f"Error in update_cache_and_db: {e}")

def get_top_50():
    """
    Return the top 50 cryptos by market cap from the in-memory cache.
    """
    all_coins = crypto_cache["data"]
    sorted_by_mc = sorted(
        all_coins,
        key=lambda x: x.get("quote", {}).get("USD", {}).get("market_cap", 0),
        reverse=True
    )
    return sorted_by_mc[:50]