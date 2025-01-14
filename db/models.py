# db/models.py
from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class CryptoEntry(Base):
    __tablename__ = "cryptos"

    id = Column(Integer, primary_key=True, index=True)
    coin_id = Column(Integer, index=True)  # CoinMarketCap 'id'
    name = Column(String)
    symbol = Column(String)
    cmc_rank = Column(Integer)
    price = Column(Float)
    volume_24h = Column(Float)
    percent_change_24h = Column(Float)
    market_cap = Column(Float)
    last_updated = Column(DateTime, default=datetime.utcnow)