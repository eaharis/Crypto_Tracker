# main.py

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from db.session import engine
from db.models import Base
from scheduler.jobs import start_scheduler, stop_scheduler
from router.crypto_router import crypto_router
from services.data_service import update_cache_and_db
from dotenv import load_dotenv

load_dotenv()
DEV_MODE = os.environ.get("DEV_MODE", "0").lower() in ("1", "true")

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        update_cache_and_db()  # if DEV_MODE=1, it won't hit external API
    except Exception as e:
        print(f"Initial update_cache_and_db() failed: {e}")

    # Start the scheduler
    if not DEV_MODE:
        start_scheduler()
        print("Scheduler started.")
    else:
        print("[DEV_MODE] Scheduler is disabled.")

    yield

    # Shutdown
    if not DEV_MODE:
        stop_scheduler()
        print("Scheduler stopped.")
    else:
        print("[DEV_MODE] No scheduler to stop.")

app = FastAPI(lifespan=lifespan)

# CORS for local React dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # specify domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router
app.include_router(crypto_router, prefix="")

@app.get("/")
def root():
    dev_mode_status = os.environ.get("DEV_MODE", "0").lower() in ("1", "true")
    mode_str = "DEV" if dev_mode_status else "PROD"
    return {"message": f"Crypto API (Upsert by coin_id). Current mode: {mode_str}."}