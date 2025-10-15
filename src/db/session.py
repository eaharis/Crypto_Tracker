# db/session.py

import os
import time

from psycopg2 import OperationalError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Retry logic for database connection
max_retries = 5
retry_interval = 5  # seconds

for attempt in range(max_retries):
    try:
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        print("Database connected successfully!")
        break
    except OperationalError as e:
        print(f"Database connection failed: {e}")
        print(f"Retrying in {retry_interval} seconds... (Attempt {attempt + 1}/{max_retries})")
        time.sleep(retry_interval)
else:
    raise Exception("Failed to connect to the database after multiple attempts.")