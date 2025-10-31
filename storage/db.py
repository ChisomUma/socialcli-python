import sqlite3
from pathlib import Path

# The database file will live at the project root
DB_PATH = Path(__file__).resolve().parent.parent / "socialcli.db"

def get_connection():
    """Create and return a connection to the SQLite database."""
    return sqlite3.connect(DB_PATH)

def create_table():
    """Create the posts table if it doesn't already exist."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT NOT NULL,
        platform TEXT NOT NULL,
        time TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

def add_post(message, platform, time):
    """Insert a new post into the database."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO posts (message, platform, time) VALUES (?, ?, ?)",
        (message, platform, time)
    )

    conn.commit()
    conn.close()

def get_all_posts():
    """Retrieve all saved posts."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, message, platform, time FROM posts")
    rows = cursor.fetchall()

    conn.close()
    return rows

def delete_post(post_id):
    """Delete a post once it's been sent."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()

