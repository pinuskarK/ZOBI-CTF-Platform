import os
import sqlite3

DB_PATH = "/app/data/research.db"

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
        ("researcher", "LabAccess-Temporary-2026")
    )

print("C3 database initialized successfully.")
