@echo off
REM Workout Tracker Launcher
REM Double-click this file to launch the application

cd /d "%~dp0"
python -m workout_tracker.main

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo Error launching Workout Tracker!
    echo Make sure Python and dependencies are installed.
    echo.
    pause
)
