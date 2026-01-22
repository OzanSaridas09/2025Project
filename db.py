import sqlite3
import os
from contextlib import contextmanager

@contextmanager
def db_session(db_name):
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    try:
        # Everything before the 'yield' happens when you enter the 'with' block
        yield conn
        # If the block inside 'with' finishes successfully, we commit
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.commit()
    except sqlite3.Error as e:
        # If ANY error occurs inside the 'with' block, we roll back
        conn.rollback()
        print(f"Database error: {e}")
        raise 
    finally:
        # This ALWAYS runs, ensuring the connection closes
        conn.close()
        print("Connection closed.")
# end of db_session

DB_PATH = 'instance/names.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    # 1. Create the instance folder if it's missing
    if not os.path.exists('instance'):
        os.makedirs('instance')
    
    # 2. Connect and create the table with the new columns
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS names (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            phonetic TEXT,
            origin TEXT,
            audio_path TEXT,
            comments TEXT,
            is_favorite INTEGER DEFAULT 0,
            last_viewed DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")