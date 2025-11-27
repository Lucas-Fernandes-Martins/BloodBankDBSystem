import psycopg
from psycopg_pool import ConnectionPool
import os
from contextlib import contextmanager

# Database configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5433")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "bloodbank")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

pool = ConnectionPool(conninfo=DATABASE_URL, min_size=1, max_size=10)

@contextmanager
def get_db_connection():
    with pool.connection() as conn:
        yield conn
