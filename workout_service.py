# workout_tracker/services/workout_service.py

from datetime import datetime
from ..db import get_connection


def save_workout(date, workout_type, sets_data, cardio_minutes=None, cardio_type=None, notes=None):
    """
    Save a complete workout with sets and optional cardio.

    Args:
        date: Date of workout (string, format: YYYY-MM-DD)
        workout_type: Type of workout (e.g., "Push", "Pull", "Legs", "Full Body")
        sets_data: List of dicts with keys: exercise_name, set_number, reps, weight, rpe (optional)
        cardio_minutes: Optional cardio duration in minutes
        cardio_type: Optional cardio type (e.g., "Running", "Cycling", "Walking")
        notes: Optional workout notes

    Returns:
        workout_id: The ID of the newly created workout
    """
    conn = get_connection()
    cur = conn.cursor()

    # Insert workout record
    cur.execute(
        """
        INSERT INTO workouts (date, workout_type, notes)
        VALUES (?, ?, ?)
        """,
        (date, workout_type, notes)
    )
    workout_id = cur.lastrowid

    # Insert sets
    for set_data in sets_data:
        cur.execute(
            """
            INSERT INTO sets (workout_id, exercise_name, set_number, reps, weight, rpe)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                workout_id,
                set_data['exercise_name'],
                set_data['set_number'],
                set_data['reps'],
                set_data['weight'],
                set_data.get('rpe')  # Optional
            )
        )

    # Insert cardio if provided
    if cardio_minutes and cardio_minutes > 0:
        cur.execute(
            """
            INSERT INTO cardio_sessions (workout_id, cardio_type, minutes)
            VALUES (?, ?, ?)
            """,
            (workout_id, cardio_type, cardio_minutes)
        )

    conn.commit()
    conn.close()

    return workout_id


def get_workouts(start_date=None, end_date=None, workout_type=None):
    """
    Retrieve workouts with optional filtering.

    Args:
        start_date: Optional start date filter (YYYY-MM-DD)
        end_date: Optional end date filter (YYYY-MM-DD)
        workout_type: Optional workout type filter

    Returns:
        List of workout dictionaries with summary data
    """
    conn = get_connection()
    cur = conn.cursor()

    # Build query with optional filters
    query = """
        SELECT
            w.id,
            w.date,
            w.workout_type,
            w.notes,
            COUNT(DISTINCT s.id) as total_sets,
            SUM(s.reps * s.weight) as total_volume,
            COALESCE(SUM(c.minutes), 0) as cardio_minutes
        FROM workouts w
        LEFT JOIN sets s ON w.id = s.workout_id
        LEFT JOIN cardio_sessions c ON w.id = c.workout_id
        WHERE 1=1
    """
    params = []

    if start_date:
        query += " AND w.date >= ?"
        params.append(start_date)

    if end_date:
        query += " AND w.date <= ?"
        params.append(end_date)

    if workout_type:
        query += " AND w.workout_type = ?"
        params.append(workout_type)

    query += """
        GROUP BY w.id
        ORDER BY w.date DESC
    """

    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_workout_details(workout_id):
    """
    Get detailed information about a specific workout including all sets and cardio.

    Args:
        workout_id: ID of the workout

    Returns:
        Dictionary with workout info, sets list, and cardio list
    """
    conn = get_connection()
    cur = conn.cursor()

    # Get workout info
    cur.execute(
        """
        SELECT id, date, workout_type, notes
        FROM workouts
        WHERE id = ?
        """,
        (workout_id,)
    )
    workout = cur.fetchone()

    if not workout:
        conn.close()
        return None

    # Get sets
    cur.execute(
        """
        SELECT exercise_name, set_number, reps, weight, rpe
        FROM sets
        WHERE workout_id = ?
        ORDER BY id
        """,
        (workout_id,)
    )
    sets = [dict(row) for row in cur.fetchall()]

    # Get cardio
    cur.execute(
        """
        SELECT cardio_type, minutes
        FROM cardio_sessions
        WHERE workout_id = ?
        """,
        (workout_id,)
    )
    cardio = [dict(row) for row in cur.fetchall()]

    conn.close()

    return {
        'workout': dict(workout),
        'sets': sets,
        'cardio': cardio
    }


def delete_workout(workout_id):
    """
    Delete a workout and all associated sets and cardio sessions.

    Args:
        workout_id: ID of the workout to delete

    Returns:
        True if deleted, False if workout not found
    """
    conn = get_connection()
    cur = conn.cursor()

    # Check if workout exists
    cur.execute("SELECT id FROM workouts WHERE id = ?", (workout_id,))
    if not cur.fetchone():
        conn.close()
        return False

    # Delete sets (cascading)
    cur.execute("DELETE FROM sets WHERE workout_id = ?", (workout_id,))

    # Delete cardio sessions (cascading)
    cur.execute("DELETE FROM cardio_sessions WHERE workout_id = ?", (workout_id,))

    # Delete workout
    cur.execute("DELETE FROM workouts WHERE id = ?", (workout_id,))

    conn.commit()
    conn.close()

    return True


def get_workout_types():
    """
    Get a list of all unique workout types used.

    Returns:
        List of workout type strings
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT DISTINCT workout_type
        FROM workouts
        ORDER BY workout_type
        """
    )

    types = [row[0] for row in cur.fetchall()]
    conn.close()

    return types


def get_exercises():
    """
    Get a list of all unique exercises logged.

    Returns:
        List of exercise name strings
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT DISTINCT exercise_name
        FROM sets
        ORDER BY exercise_name
        """
    )

    exercises = [row[0] for row in cur.fetchall()]
    conn.close()

    return exercises
