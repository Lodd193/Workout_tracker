# Quick Start Guide

Get up and running with Workout Tracker in 5 minutes!

## Step 1: Install Python

Make sure you have Python 3.8 or higher installed:
```bash
python --version
```

If not installed, download from [python.org](https://www.python.org/downloads/)

## Step 2: Install Dependencies

Navigate to the project directory and install requirements:

```bash
cd workout_tracker
pip install -r workout_tracker/requirements.txt
```

## Step 3: Run the Application

```bash
python -m workout_tracker.main
```

The application window will open with the "superhero" theme.

## Step 4: Log Your First Workout

1. The app opens on the **Log Workout** tab
2. Select today's date (pre-filled)
3. Choose a workout type (e.g., "Push")
4. Enter an exercise:
   - Exercise: Bench Press
   - Reps: 8
   - Weight: 135
   - RPE: 7
5. Click **Add Set**
6. Repeat for more sets/exercises
7. (Optional) Add cardio minutes
8. Click **Save Workout**

## Step 5: View Your History

1. Click the **History** tab
2. See your workout in the table
3. Double-click to view full details

## Step 6: Analyze Your Progress

1. Click the **Analytics** tab
2. Select an exercise from the dropdown
3. View progression chart
4. Check weekly volume trends
5. Monitor cardio goal progress

## Step 7: Export Your Data

1. In the **Analytics** tab, scroll to bottom
2. Click **Export All Data**
3. Choose a directory
4. Three CSV files will be created

## Troubleshooting

### "Module not found" error
Make sure you installed dependencies:
```bash
pip install -r workout_tracker/requirements.txt
```

### Database not created
The database (workouts.db) is created automatically on first run in the `workout_tracker/` directory.

### Application won't start
Verify you're in the correct directory:
```bash
ls workout_tracker/
# Should show: main.py, db.py, services/, ui/, etc.
```

## Next Steps

- Read the full [README.md](README.md) for detailed features
- Check [FEATURES.md](FEATURES.md) for complete feature list
- Customize the theme in `main.py` (line 12)

## Tips

- **Keyboard shortcut**: Tab through fields for faster data entry
- **RPE is optional**: Leave blank if you don't track it
- **Double-click**: In History tab, double-click workouts for quick details
- **Filter smartly**: Use date range filters to analyze specific training blocks
- **Export regularly**: Back up your data with the export feature

## Common Workout Types

Pre-configured options:
- Push (Chest, Shoulders, Triceps)
- Pull (Back, Biceps)
- Legs
- Full Body
- Upper
- Lower
- Cardio
- Other

## Sample Exercises

Try logging these common exercises:
- Bench Press
- Squat
- Deadlift
- Overhead Press
- Barbell Row
- Pull-ups
- Dumbbell Curl
- Lateral Raise

---

**Enjoy tracking your fitness journey! 💪**
