"""Ensure required directories exist."""
import os

db_path = os.environ.get("DB_PATH", "/app/news.db")
os.makedirs(os.path.dirname(db_path), exist_ok=True)
print("Startup complete")
