# workout_tracker/export.py

import csv
from pathlib import Path
from datetime import datetime
from .db import get_connection


def export_workouts_to_csv(output_path):
    """
    Export all workouts to a CSV file.

    Args:
        output_path: Path to the output CSV file

    Returns:
        Number of workouts exported
    """
    conn = get_connection()
    cur = conn.cursor()

    # Get all workouts with summary data
    cur.execute(
        """
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
        GROUP BY w.id
        ORDER BY w.date DESC
        """
    )

    workouts = cur.fetchall()
    conn.close()

    # Write to CSV
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Write header
        writer.writerow([
            'Workout ID',
            'Date',
            'Workout Type',
            'Total Sets',
            'Total Volume (lbs)',
            'Cardio Minutes',
            'Notes'
        ])

        # Write data
        for workout in workouts:
            writer.writerow([
                workout['id'],
                workout['date'],
                workout['workout_type'],
                workout['total_sets'] or 0,
                f"{workout['total_volume']:.2f}" if workout['total_volume'] else "0.00",
                workout['cardio_minutes'] or 0,
                workout['notes'] or ''
            ])

    return len(workouts)


def export_sets_to_csv(output_path):
    """
    Export all sets to a CSV file.

    Args:
        output_path: Path to the output CSV file

    Returns:
        Number of sets exported
    """
    conn = get_connection()
    cur = conn.cursor()

    # Get all sets with workout info
    cur.execute(
        """
        SELECT
            s.id,
            w.date,
            w.workout_type,
            s.exercise_name,
            s.set_number,
            s.reps,
            s.weight,
            s.rpe,
            w.id as workout_id
        FROM sets s
        JOIN workouts w ON s.workout_id = w.id
        ORDER BY w.date DESC, s.id ASC
        """
    )

    sets = cur.fetchall()
    conn.close()

    # Write to CSV
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Write header
        writer.writerow([
            'Set ID',
            'Workout ID',
            'Date',
            'Workout Type',
            'Exercise',
            'Set Number',
            'Reps',
            'Weight (lbs)',
            'RPE'
        ])

        # Write data
        for set_row in sets:
            writer.writerow([
                set_row['id'],
                set_row['workout_id'],
                set_row['date'],
                set_row['workout_type'],
                set_row['exercise_name'],
                set_row['set_number'],
                set_row['reps'],
                set_row['weight'],
                set_row['rpe'] if set_row['rpe'] else ''
            ])

    return len(sets)


def export_cardio_to_csv(output_path):
    """
    Export all cardio sessions to a CSV file.

    Args:
        output_path: Path to the output CSV file

    Returns:
        Number of cardio sessions exported
    """
    conn = get_connection()
    cur = conn.cursor()

    # Get all cardio sessions with workout info
    cur.execute(
        """
        SELECT
            c.id,
            w.date,
            w.workout_type,
            c.cardio_type,
            c.minutes,
            w.id as workout_id
        FROM cardio_sessions c
        JOIN workouts w ON c.workout_id = w.id
        ORDER BY w.date DESC
        """
    )

    cardio_sessions = cur.fetchall()
    conn.close()

    # Write to CSV
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Write header
        writer.writerow([
            'Cardio ID',
            'Workout ID',
            'Date',
            'Workout Type',
            'Cardio Type',
            'Minutes'
        ])

        # Write data
        for cardio in cardio_sessions:
            writer.writerow([
                cardio['id'],
                cardio['workout_id'],
                cardio['date'],
                cardio['workout_type'],
                cardio['cardio_type'] or 'General',
                cardio['minutes']
            ])

    return len(cardio_sessions)


def export_all_data(output_dir):
    """
    Export all workout data to separate CSV files in the specified directory.

    Args:
        output_dir: Directory path where CSV files will be saved

    Returns:
        Dictionary with counts of exported records
    """
    # Ensure output directory exists
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Generate timestamped filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    workouts_file = output_path / f"workouts_{timestamp}.csv"
    sets_file = output_path / f"sets_{timestamp}.csv"
    cardio_file = output_path / f"cardio_{timestamp}.csv"

    # Export each dataset
    workouts_count = export_workouts_to_csv(workouts_file)
    sets_count = export_sets_to_csv(sets_file)
    cardio_count = export_cardio_to_csv(cardio_file)

    return {
        'workouts': workouts_count,
        'sets': sets_count,
        'cardio': cardio_count,
        'workouts_file': str(workouts_file),
        'sets_file': str(sets_file),
        'cardio_file': str(cardio_file)
    }


def export_exercise_data(exercise_name, output_path):
    """
    Export all sets for a specific exercise to CSV.

    Args:
        exercise_name: Name of the exercise
        output_path: Path to the output CSV file

    Returns:
        Number of sets exported
    """
    conn = get_connection()
    cur = conn.cursor()

    # Get all sets for the exercise
    cur.execute(
        """
        SELECT
            s.id,
            w.date,
            w.workout_type,
            s.exercise_name,
            s.set_number,
            s.reps,
            s.weight,
            s.rpe,
            w.notes
        FROM sets s
        JOIN workouts w ON s.workout_id = w.id
        WHERE s.exercise_name = ?
        ORDER BY w.date ASC
        """,
        (exercise_name,)
    )

    sets = cur.fetchall()
    conn.close()

    # Write to CSV
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Write header
        writer.writerow([
            'Set ID',
            'Date',
            'Workout Type',
            'Exercise',
            'Set Number',
            'Reps',
            'Weight (lbs)',
            'RPE',
            'Workout Notes'
        ])

        # Write data
        for set_row in sets:
            writer.writerow([
                set_row['id'],
                set_row['date'],
                set_row['workout_type'],
                set_row['exercise_name'],
                set_row['set_number'],
                set_row['reps'],
                set_row['weight'],
                set_row['rpe'] if set_row['rpe'] else '',
                set_row['notes'] or ''
            ])

    return len(sets)


def export_date_range(start_date, end_date, output_dir):
    """
    Export workouts within a date range to CSV files.

    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        output_dir: Directory path where CSV files will be saved

    Returns:
        Dictionary with counts of exported records
    """
    # Ensure output directory exists
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Generate filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    workouts_file = output_path / f"workouts_{start_date}_to_{end_date}_{timestamp}.csv"

    conn = get_connection()
    cur = conn.cursor()

    # Get workouts in date range
    cur.execute(
        """
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
        WHERE w.date BETWEEN ? AND ?
        GROUP BY w.id
        ORDER BY w.date DESC
        """,
        (start_date, end_date)
    )

    workouts = cur.fetchall()
    conn.close()

    # Write to CSV
    with open(workouts_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Write header
        writer.writerow([
            'Workout ID',
            'Date',
            'Workout Type',
            'Total Sets',
            'Total Volume (lbs)',
            'Cardio Minutes',
            'Notes'
        ])

        # Write data
        for workout in workouts:
            writer.writerow([
                workout['id'],
                workout['date'],
                workout['workout_type'],
                workout['total_sets'] or 0,
                f"{workout['total_volume']:.2f}" if workout['total_volume'] else "0.00",
                workout['cardio_minutes'] or 0,
                workout['notes'] or ''
            ])

    return {
        'workouts': len(workouts),
        'workouts_file': str(workouts_file),
        'start_date': start_date,
        'end_date': end_date
    }
