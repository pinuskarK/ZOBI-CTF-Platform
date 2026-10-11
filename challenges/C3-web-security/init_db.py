import os
import sqlite3

DB_PATH = os.environ.get("C3_DB_PATH", "/app/data/research.db")
USERNAME = os.environ.get("C3_DEMO_USERNAME", "researcher")
PASSWORD = os.environ.get("C3_DEMO_PASSWORD")
if not PASSWORD:
    raise RuntimeError("C3_DEMO_PASSWORD must be set in the environment")

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

with sqlite3.connect(DB_PATH) as connection:
    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)
    connection.execute(
        "INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
        (USERNAME, PASSWORD),
    )

print("C3 database initialized successfully.")
