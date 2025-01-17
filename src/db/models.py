# db/models.py

from sqlalchemy import Column, Integer, Float, String, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class CryptoEntry(Base):
    __tablename__ = "cryptos"

    # By making coin_id the primary key, each row is uniquely identified
    # by the coin's ID from CoinMarketCap. We'll upsert on this key.
    coin_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    symbol = Column(String)
    cmc_rank = Column(Integer)
    price = Column(Float)
    volume_24h = Column(Float)
    percent_change_24h = Column(Float)
    market_cap = Column(Float)
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())