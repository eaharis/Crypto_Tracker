# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from db.session import engine
from db.models import Base
from services.data_service import update_cache_and_db
from scheduler.jobs import start_scheduler, stop_scheduler
from router.crypto_router import crypto_router
from services.data_service import load_data_from_db_into_cache

# 1) Create tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # First: do an immediate fetch & update so DB is never empty
    # If you'd rather load existing data from DB, you can do that first
    try:
        update_cache_and_db(limit=50)
    except Exception as e:
        print(f"Initial fetch failed: {e}")

    # Then start APScheduler
    start_scheduler()
    print("Scheduler started.")

    yield  # ---- The app runs here ----

    # On shutdown
    stop_scheduler()
    print("Scheduler stopped.")

app = FastAPI(lifespan=lifespan)

# CORS for local React dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify a domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router
app.include_router(crypto_router, prefix="")

@app.get("/")
def root():
    return {"message": "Crypto API with DB & Cache is running."}