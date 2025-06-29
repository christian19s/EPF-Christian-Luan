import os
import sqlite3
from contextlib import closing
from pathlib import Path

# Get absolute path to data directory
BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = BASE_DIR / "db"
DB_PATH = DATA_DIR / "wiki.db"
SCHEMA_PATH = DATA_DIR / "schema.sql"


def get_db_connection():
    """Return SQLite connection with foreign keys enabled"""
    # Create data directory if missing
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    with closing(get_db_connection()) as conn:
        # Only create if schema exists
        if SCHEMA_PATH.exists():
            with open(SCHEMA_PATH, "r") as f:
                conn.executescript(f.read())
            conn.commit()
            print(f" Database initialized at: {DB_PATH}")
        else:
            print(f"Schema file not found at {SCHEMA_PATH}")


if __name__ == "__main__":
    init_db()
