# workout_tracker/services/analytics_service.py

from datetime import datetime, timedelta
from collections import defaultdict
from ..db import get_connection


def get_exercise_progression(exercise_name):
    """
    Get progression data for a specific exercise over time.

    Args:
        exercise_name: Name of the exercise

    Returns:
        List of dicts with date, max_weight, total_volume, total_reps
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            w.date,
            MAX(s.weight) as max_weight,
            SUM(s.reps * s.weight) as total_volume,
            SUM(s.reps) as total_reps,
            COUNT(s.id) as num_sets
        FROM sets s
        JOIN workouts w ON s.workout_id = w.id
        WHERE s.exercise_name = ?
        GROUP BY w.date
        ORDER BY w.date ASC
        """,
        (exercise_name,)
    )

    rows = cur.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_top_set_by_date(exercise_name):
    """
    Get the top (heaviest) set for each date for a specific exercise.

    Args:
        exercise_name: Name of the exercise

    Returns:
        List of dicts with date, weight, reps, rpe
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            w.date,
            s.weight,
            s.reps,
            s.rpe
        FROM sets s
        JOIN workouts w ON s.workout_id = w.id
        WHERE s.exercise_name = ?
        AND s.weight = (
            SELECT MAX(s2.weight)
            FROM sets s2
            JOIN workouts w2 ON s2.workout_id = w2.id
            WHERE s2.exercise_name = s.exercise_name
            AND w2.date = w.date
        )
        GROUP BY w.date
        ORDER BY w.date ASC
        """,
        (exercise_name,)
    )

    rows = cur.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_weekly_volume(weeks=12):
    """
    Calculate total weekly volume (weight × reps) for the last N weeks.

    Args:
        weeks: Number of weeks to analyze (default 12)

    Returns:
        List of dicts with week_start_date and total_volume
    """
    conn = get_connection()
    cur = conn.cursor()

    # Calculate start date
    end_date = datetime.now()
    start_date = end_date - timedelta(weeks=weeks)

    cur.execute(
        """
        SELECT
            date(w.date, 'weekday 0', '-6 days') as week_start,
            SUM(s.reps * s.weight) as total_volume
        FROM sets s
        JOIN workouts w ON s.workout_id = w.id
        WHERE w.date >= ?
        GROUP BY week_start
        ORDER BY week_start ASC
        """,
        (start_date.strftime('%Y-%m-%d'),)
    )

    rows = cur.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_cardio_weekly_summary(weeks=12):
    """
    Get weekly cardio minutes for the last N weeks.

    Args:
        weeks: Number of weeks to analyze (default 12)

    Returns:
        List of dicts with week_start_date, total_minutes, workout_count
    """
    conn = get_connection()
    cur = conn.cursor()

    # Calculate start date
    end_date = datetime.now()
    start_date = end_date - timedelta(weeks=weeks)

    cur.execute(
        """
        SELECT
            date(w.date, 'weekday 0', '-6 days') as week_start,
            SUM(c.minutes) as total_minutes,
            COUNT(DISTINCT c.workout_id) as workout_count
        FROM cardio_sessions c
        JOIN workouts w ON c.workout_id = w.id
        WHERE w.date >= ?
        GROUP BY week_start
        ORDER BY week_start ASC
        """,
        (start_date.strftime('%Y-%m-%d'),)
    )

    rows = cur.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_current_week_cardio():
    """
    Get total cardio minutes for the current week (Monday-Sunday).

    Returns:
        Integer representing total minutes this week
    """
    conn = get_connection()
    cur = conn.cursor()

    # Get the Monday of the current week
    today = datetime.now()
    monday = today - timedelta(days=today.weekday())
    monday_str = monday.strftime('%Y-%m-%d')

    cur.execute(
        """
        SELECT COALESCE(SUM(c.minutes), 0) as total_minutes
        FROM cardio_sessions c
        JOIN workouts w ON c.workout_id = w.id
        WHERE w.date >= ?
        """,
        (monday_str,)
    )

    result = cur.fetchone()
    conn.close()

    return result[0] if result else 0


def get_exercise_volume_by_type():
    """
    Get total volume grouped by exercise for all time.

    Returns:
        List of dicts with exercise_name, total_volume, total_sets, total_reps
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            s.exercise_name,
            SUM(s.reps * s.weight) as total_volume,
            COUNT(s.id) as total_sets,
            SUM(s.reps) as total_reps,
            AVG(s.weight) as avg_weight
        FROM sets s
        GROUP BY s.exercise_name
        ORDER BY total_volume DESC
        """
    )

    rows = cur.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def calculate_estimated_1rm(weight, reps):
    """
    Calculate estimated 1RM using the Epley formula.

    Args:
        weight: Weight lifted
        reps: Number of reps performed

    Returns:
        Estimated 1RM value
    """
    if reps == 1:
        return weight
    # Epley formula: 1RM = weight × (1 + reps/30)
    return weight * (1 + reps / 30)


def get_estimated_1rm_progression(exercise_name):
    """
    Get estimated 1RM progression over time for an exercise.

    Args:
        exercise_name: Name of the exercise

    Returns:
        List of dicts with date, estimated_1rm, actual_weight, reps
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            w.date,
            s.weight,
            s.reps,
            s.rpe
        FROM sets s
        JOIN workouts w ON s.workout_id = w.id
        WHERE s.exercise_name = ?
        ORDER BY w.date ASC
        """,
        (exercise_name,)
    )

    rows = cur.fetchall()
    conn.close()

    # Calculate estimated 1RM for each set
    progression = []
    for row in rows:
        row_dict = dict(row)
        estimated_1rm = calculate_estimated_1rm(row_dict['weight'], row_dict['reps'])
        progression.append({
            'date': row_dict['date'],
            'estimated_1rm': round(estimated_1rm, 2),
            'actual_weight': row_dict['weight'],
            'reps': row_dict['reps'],
            'rpe': row_dict['rpe']
        })

    return progression


def get_personal_records(exercise_name=None):
    """
    Get personal records (max weight) for exercises.

    Args:
        exercise_name: Optional specific exercise, or None for all exercises

    Returns:
        List of dicts with exercise_name, max_weight, reps, date
    """
    conn = get_connection()
    cur = conn.cursor()

    if exercise_name:
        cur.execute(
            """
            SELECT
                s.exercise_name,
                s.weight as max_weight,
                s.reps,
                w.date
            FROM sets s
            JOIN workouts w ON s.workout_id = w.id
            WHERE s.exercise_name = ?
            AND s.weight = (
                SELECT MAX(weight)
                FROM sets
                WHERE exercise_name = s.exercise_name
            )
            LIMIT 1
            """,
            (exercise_name,)
        )
    else:
        cur.execute(
            """
            SELECT
                s.exercise_name,
                MAX(s.weight) as max_weight,
                s.reps,
                w.date
            FROM sets s
            JOIN workouts w ON s.workout_id = w.id
            WHERE (s.exercise_name, s.weight) IN (
                SELECT exercise_name, MAX(weight)
                FROM sets
                GROUP BY exercise_name
            )
            GROUP BY s.exercise_name
            ORDER BY s.exercise_name
            """
        )

    rows = cur.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_workout_frequency(days=30):
    """
    Calculate workout frequency for the last N days.

    Args:
        days: Number of days to analyze (default 30)

    Returns:
        Dict with total_workouts, days_analyzed, avg_per_week
    """
    conn = get_connection()
    cur = conn.cursor()

    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    cur.execute(
        """
        SELECT COUNT(*) as workout_count
        FROM workouts
        WHERE date >= ?
        """,
        (start_date.strftime('%Y-%m-%d'),)
    )

    result = cur.fetchone()
    conn.close()

    workout_count = result[0] if result else 0
    avg_per_week = (workout_count / days) * 7 if days > 0 else 0

    return {
        'total_workouts': workout_count,
        'days_analyzed': days,
        'avg_per_week': round(avg_per_week, 2)
    }
