import os
import sqlite3
from contextlib import closing
from os.path import exists
from pathlib import Path

BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = BASE_DIR / "db"
UPLOAD_DIR = BASE_DIR / "uploads"
USER_UPLOADS = UPLOAD_DIR / "users"
WIKI_UPLOADS = UPLOAD_DIR / "wiki"
DB_PATH = DATA_DIR / "wiki.db"
SCHEMA_PATH = DATA_DIR / "schema.sql"


def get_user_upload_path():
    return USER_UPLOADS


def get_wiki_upload_path():
    return WIKI_UPLOADS


def get_db_connection():
    """Return SQLite connection with foreign keys enabled"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    print(f"Creating upload directories at: {USER_UPLOADS}, {WIKI_UPLOADS}")
    try:
        USER_UPLOADS.mkdir(parents=True, exist_ok=True)
        WIKI_UPLOADS.mkdir(parents=True, exist_ok=True)
        print(f"User upload directory: {USER_UPLOADS}")
        print(f"Directory exists: {USER_UPLOADS.exists()}")
        print(f"Directory exists: {WIKI_UPLOADS.exists()}")
        print(f"Directory writable {USER_UPLOADS}: {os.access(USER_UPLOADS, os.W_OK)}")
        print(f"Directory writable {WIKI_UPLOADS}: {os.access(USER_UPLOADS, os.W_OK)}")
    except Exception as e:
        print(f"Directory creation error: {str(e)}")
        with closing(get_db_connection()) as conn:
            if SCHEMA_PATH.exists():
                with open(SCHEMA_PATH, "r") as f:
                    conn.executescript(f.read())
                conn.commit()
                print(f" Database initialized at: {DB_PATH}")
            else:
                print(f"Schema file not found at {SCHEMA_PATH}")
        if __name__ == "__main__":
            init_db()
