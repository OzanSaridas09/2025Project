import sqlite3
from contextlib import contextmanager

@contextmanager
def db_session(db_name):
    conn = sqlite3.connect(db_name)
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

def init_db():
    """
    Initializes the SQLite database by creating the necessary tables 
    if they do not already exist.
    """
    # Use the 'instance/' folder path to keep the database separate from code
    db_path = 'instance/names.db'
    
    with db_session(db_path) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS names (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                phonetic TEXT,
                origin TEXT,
                comments TEXT,
                audio_path TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    print("Database tables created successfully.")

if __name__ == "__main__":
    import os
    # Create the instance folder if it doesn't exist to prevent 'File Not Found' errors
    if not os.path.exists('instance'):
        os.makedirs('instance')
        print("Created 'instance' directory.")
        
    init_db()