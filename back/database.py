import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "resources.db"

def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row # Allow rows to be accessible like in a dictionnary (more readable)
    return conn