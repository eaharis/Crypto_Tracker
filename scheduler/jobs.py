# scheduler/jobs.py
from apscheduler.schedulers.background import BackgroundScheduler
from services.data_service import update_cache_and_db

scheduler = BackgroundScheduler()

def start_scheduler():
    # Schedule update every 15 minutes
    scheduler.add_job(update_cache_and_db, "interval", minutes=15)
    scheduler.start()

def stop_scheduler():
    scheduler.shutdown()