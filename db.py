# workout_tracker/db.py

import sqlite3
from pathlib import Path

# SQLite database file in the same folder as db.py
DB_PATH = Path(__file__).resolve().parent / "workouts.db"


def get_connection():
    """Return a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # return rows as dictionaries
    return conn


def create_tables():
    """Create the database tables if they don't already exist."""
    conn = get_connection()
    cur = conn.cursor()

    # Workouts table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            workout_type TEXT NOT NULL,
            name TEXT,
            notes TEXT
        );
        """
    )

    # Sets table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workout_id INTEGER NOT NULL,
            exercise_name TEXT NOT NULL,
            set_number INTEGER NOT NULL,
            reps INTEGER NOT NULL,
            weight REAL NOT NULL,
            rpe REAL,
            FOREIGN KEY (workout_id) REFERENCES workouts(id)
        );
        """
    )

    # Cardio sessions table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS cardio_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workout_id INTEGER NOT NULL,
            cardio_type TEXT,
            minutes INTEGER NOT NULL,
            FOREIGN KEY (workout_id) REFERENCES workouts(id)
        );
        """
    )

    conn.commit()
    conn.close()
