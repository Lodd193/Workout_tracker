# workout_tracker/services/__init__.py
"""Services package for workout tracker business logic."""

from .workout_service import (
    save_workout,
    get_workouts,
    get_workout_details,
    delete_workout,
    get_workout_types,
    get_exercises
)

from .analytics_service import (
    get_exercise_progression,
    get_top_set_by_date,
    get_weekly_volume,
    get_cardio_weekly_summary,
    get_current_week_cardio,
    get_exercise_volume_by_type,
    calculate_estimated_1rm,
    get_estimated_1rm_progression,
    get_personal_records,
    get_workout_frequency
)

__all__ = [
    # Workout service
    'save_workout',
    'get_workouts',
    'get_workout_details',
    'delete_workout',
    'get_workout_types',
    'get_exercises',
    # Analytics service
    'get_exercise_progression',
    'get_top_set_by_date',
    'get_weekly_volume',
    'get_cardio_weekly_summary',
    'get_current_week_cardio',
    'get_exercise_volume_by_type',
    'calculate_estimated_1rm',
    'get_estimated_1rm_progression',
    'get_personal_records',
    'get_workout_frequency',
]
