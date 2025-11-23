# Workout Tracker - Complete Operation Guide

**Version**: 1.0.0
**Last Updated**: November 23, 2025
**Status**: Production Ready ✅

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Installation](#installation)
3. [Running the Application](#running-the-application)
4. [User Interface Guide](#user-interface-guide)
5. [Logging Your First Workout](#logging-your-first-workout)
6. [Viewing History](#viewing-history)
7. [Analyzing Progress](#analyzing-progress)
8. [Exporting Data](#exporting-data)
9. [Testing](#testing)
10. [Building Executable](#building-executable)
11. [Troubleshooting](#troubleshooting)
12. [Advanced Features](#advanced-features)

---

## Quick Start

### Prerequisites
- Windows, macOS, or Linux
- Python 3.8 or higher
- pip (Python package manager)

### Install & Run (3 steps)

```bash
# 1. Install dependencies
cd workout_tracker
pip install -r workout_tracker/requirements.txt

# 2. Run the application
python -m workout_tracker.main

# 3. Start logging workouts!
```

---

## Installation

### Step 1: Verify Python Installation

```bash
python --version
# Should show Python 3.8 or higher
```

If Python is not installed:
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- **macOS**: Use Homebrew: `brew install python3`
- **Linux**: Use package manager: `sudo apt install python3 python3-pip`

### Step 2: Navigate to Project Directory

```bash
cd /path/to/workout_tracker
```

### Step 3: Install Dependencies

```bash
pip install -r workout_tracker/requirements.txt
```

**Dependencies installed**:
- ttkbootstrap (modern UI)
- matplotlib (charts)
- pandas (data analysis)
- python-dateutil (date utilities)

### Step 4: Verify Installation

```bash
python -c "import ttkbootstrap; print('Installation successful!')"
```

---

## Running the Application

### Method 1: Python Module (Recommended)

```bash
python -m workout_tracker.main
```

### Method 2: Direct Script

```bash
python workout_tracker/main.py
```

### What Happens on First Run

1. **Database Creation**: `workout_tracker/workouts.db` is created automatically
2. **Window Opens**: Main application window (1000x700 pixels)
3. **Theme Applied**: "superhero" dark theme loads
4. **Tabs Appear**: Log Workout, History, Analytics tabs ready to use

---

## User Interface Guide

### Main Window Layout

```
┌─────────────────────────────────────────────┐
│  Workout Tracker                       ─ □ ×│
├─────────────────────────────────────────────┤
│ [Log Workout] [History] [Analytics]         │
├─────────────────────────────────────────────┤
│                                             │
│         (Active Tab Content)                │
│                                             │
│                                             │
└─────────────────────────────────────────────┘
```

### Tab 1: Log Workout

**Purpose**: Record your workout sessions

**Sections**:
1. **Workout Information**: Date and workout type
2. **Exercises & Sets**: Add exercises with details
3. **Cardio**: Optional cardio tracking
4. **Notes**: Optional workout notes
5. **Actions**: Save or Clear

### Tab 2: History

**Purpose**: View and manage past workouts

**Features**:
- Filter by date range
- Filter by workout type
- View workout summaries
- Double-click for details
- Delete workouts

### Tab 3: Analytics

**Purpose**: Visualize your progress

**Charts**:
- Lift progression (line chart)
- Weekly volume (bar chart)
- Cardio goal tracker
- Personal records

---

## Logging Your First Workout

### Example: Chest Day (Push Workout)

#### Step 1: Select Date and Type

1. Click **Log Workout** tab
2. Date: Select today (pre-filled)
3. Workout Type: Choose **"Push"**

#### Step 2: Add First Exercise (Bench Press)

1. Exercise: Type **"Bench Press"**
2. Reps: Enter **8**
3. Weight: Enter **135**
4. RPE: Enter **7** (optional)
5. Click **"Add Set"**

**Result**: Set 1 appears in the table below

#### Step 3: Add More Sets

Repeat for additional sets:
- Set 2: 8 reps @ 135 lbs, RPE 8
- Set 3: 8 reps @ 135 lbs, RPE 9

#### Step 4: Add Second Exercise (Overhead Press)

1. Exercise: Change to **"Overhead Press"**
2. Reps: Enter **10**
3. Weight: Enter **95**
4. RPE: Enter **7**
5. Click **"Add Set"**

#### Step 5: Add Cardio (Optional)

1. Cardio Type: Select **"Walking"**
2. Minutes: Enter **20**

#### Step 6: Add Notes (Optional)

```
Good session! Felt strong on bench press.
Added extra set on overhead press.
```

#### Step 7: Save Workout

1. Click **"Save Workout"**
2. Success dialog appears: "Workout saved successfully!"
3. Form clears automatically

---

## Viewing History

### Opening History Tab

1. Click **History** tab
2. Workouts load automatically (last 30 days)

### Filtering Workouts

#### By Date Range

1. Set **From**: 2025-01-01
2. Set **To**: 2025-12-31
3. Click **"Apply Filters"**

#### By Workout Type

1. Select type from dropdown: **"Push"**
2. Click **"Apply Filters"**

#### Clear Filters

Click **"Clear Filters"** to reset to default (last 30 days)

### Viewing Workout Details

**Method 1**: Double-click any workout row

**Method 2**:
1. Click to select workout
2. Click **"View Details"** button

**Details Popup Shows**:
- Date and workout type
- All exercises and sets
- Cardio sessions
- Workout notes

### Deleting a Workout

1. Click to select workout
2. Click **"Delete Workout"**
3. Confirm deletion (this cannot be undone)
4. Workout removed from history

---

## Analyzing Progress

### Lift Progression Chart

#### View Progression

1. Click **Analytics** tab
2. Select exercise from dropdown: **"Bench Press"**
3. Chart updates automatically

#### Chart Types

**Max Weight** (default):
- Shows heaviest lift per session
- Tracks strength progression over time

**Total Volume**:
- Shows total weight × reps per session
- Tracks work capacity over time

#### Using Chart Tools

**Zoom In**: Click magnifying glass icon, drag area
**Pan**: Click hand icon, drag chart
**Reset**: Click home icon
**Save**: Click save icon to save as image

### Weekly Volume Chart

#### View Volume Trends

1. Chart displays last 12 weeks by default
2. Purple bars show total weekly volume
3. Numbers on bars show exact values

#### Change Time Range

1. Adjust **Weeks** spinbox (4-24)
2. Click **"Update"**
3. Chart refreshes with new range

### Cardio Goal Tracker

#### Check Progress

- **Current week** minutes displayed
- **Goal**: 150 minutes per week
- **Progress bar** color-coded:
  - Blue: 0-50% (0-75 mins)
  - Orange: 50-99% (75-149 mins)
  - Green: 100%+ (150+ mins)

#### Refresh

Click **"Refresh"** to update with latest data

### Personal Records

View your PRs for all exercises:
- Click **"Refresh PRs"**
- Top 5 PRs displayed
- Shows exercise name and max weight

---

## Exporting Data

### Export All Data

#### Step 1: Click Export

1. Scroll to bottom of **Analytics** tab
2. Click **"Export All Data"**

#### Step 2: Select Directory

1. File browser opens
2. Navigate to desired save location
3. Click **"Select Folder"**

#### Step 3: Review Export

**3 CSV files created**:
- `workouts_TIMESTAMP.csv` (summary data)
- `sets_TIMESTAMP.csv` (all exercise sets)
- `cardio_TIMESTAMP.csv` (cardio sessions)

**Success Dialog Shows**:
- Number of workouts exported
- Number of sets exported
- Number of cardio sessions exported
- Save location

### Export Specific Exercise

#### Step 1: Select Exercise

1. Choose exercise from dropdown: **"Bench Press"**

#### Step 2: Click Export

Click **"Export Exercise"**

#### Step 3: Save File

1. File browser opens
2. Default name: `Bench_Press_data.csv`
3. Choose location
4. Click **"Save"**

#### CSV Contents

All sets for that exercise with:
- Date
- Workout type
- Set number
- Reps, weight, RPE
- Workout notes

### Opening Exported Files

**Excel / Google Sheets**:
- Open application
- File → Open
- Select CSV file

**Python / Pandas**:
```python
import pandas as pd
df = pd.read_csv('workouts_20251123_120000.csv')
print(df.head())
```

---

## Testing

### Running Unit Tests

#### Install Test Dependencies

```bash
pip install -r requirements-dev.txt
```

#### Run All Tests

```bash
# Basic test run
pytest

# With coverage report
pytest --cov=workout_tracker

# Verbose output
pytest -v

# Specific test file
pytest tests/test_workout_service.py
```

#### Test Results

**Expected Output**:
```
============================= test session starts ==============================
collected 23 items

tests/test_workout_service.py ............ [ 52%]
tests/test_analytics_service.py ........... [100%]

============================== 23 passed in 2.34s ===============================
```

#### Coverage Report

```bash
pytest --cov=workout_tracker --cov-report=html
# Open htmlcov/index.html in browser
```

---

## Building Executable

### Create Standalone Application

#### Step 1: Install PyInstaller

```bash
pip install pyinstaller
```

#### Step 2: Build Application

```bash
pyinstaller workout_tracker.spec
```

#### Step 3: Locate Executable

**Output location**: `dist/`

**Files**:
- **Windows**: `WorkoutTracker.exe`
- **macOS**: `WorkoutTracker.app`
- **Linux**: `WorkoutTracker`

#### Step 4: Test Executable

```bash
cd dist
./WorkoutTracker  # Linux/macOS
# or double-click WorkoutTracker.exe on Windows
```

#### Distribution

The executable is **standalone** and can be:
- Copied to any computer (same OS)
- Shared with others
- Run without Python installed

**Note**: Build on each target platform (no cross-compilation)

---

## Troubleshooting

### Application Won't Start

#### Problem: "ModuleNotFoundError"

**Solution**:
```bash
pip install -r workout_tracker/requirements.txt
```

#### Problem: "No module named 'workout_tracker'"

**Solution**: Run from project root:
```bash
cd /path/to/workout_tracker
python -m workout_tracker.main
```

#### Problem: Database error on startup

**Solution**: Database creates automatically. Check permissions:
```bash
ls -la workout_tracker/
# Ensure you have write permissions
```

### Import Errors

#### Problem: "ImportError: cannot import name..."

**Solution**: Verify all files exist:
```bash
ls workout_tracker/*.py
ls workout_tracker/services/*.py
ls workout_tracker/ui/*.py
```

### UI Issues

#### Problem: Window is too small/large

**Solution**: Edit `workout_tracker/main.py`, line 14:
```python
app.geometry("1000x700")  # Change dimensions
```

#### Problem: Theme looks wrong

**Solution**: Change theme in `workout_tracker/main.py`, line 12:
```python
app = Window(themename="superhero")
# Try: "darkly", "solar", "cyborg", "vapor"
```

### Data Issues

#### Problem: Workouts not appearing in History

**Solution**:
1. Check date filter range
2. Click "Clear Filters"
3. Verify workout was saved (check success dialog)

#### Problem: Charts show no data

**Solution**:
1. Ensure workouts are logged
2. Select correct exercise
3. Click "Update" button
4. Check database exists: `ls workout_tracker/workouts.db`

### Export Issues

#### Problem: Export fails with permission error

**Solution**:
1. Choose different directory
2. Ensure you have write permissions
3. Close CSV if open in Excel

#### Problem: CSV file is empty

**Solution**: Log some workouts first, then export

---

## Advanced Features

### Database Location

**Default**: `workout_tracker/workouts.db`

**To change**: Edit `workout_tracker/db.py`, line 7:
```python
DB_PATH = Path(__file__).resolve().parent / "workouts.db"
```

### Custom Themes

**Available themes**:
- superhero (default - dark blue)
- darkly (dark gray)
- cyborg (dark with cyan)
- solar (dark warm)
- vapor (pink/purple)
- cosmo (light blue)
- flatly (light green)

**Change in**: `workout_tracker/main.py`, line 12

### Customizing Window Size

Edit `workout_tracker/main.py`:
```python
app.geometry("1200x800")  # Larger
app.geometry("800x600")   # Smaller
```

### Adding Workout Types

Edit `workout_tracker/ui/log_workout_view.py`, line 54:
```python
values=["Push", "Pull", "Legs", "Full Body", "Upper", "Lower", "Cardio", "Other", "Your Custom Type"]
```

### Backup Your Data

**Method 1**: Copy database file
```bash
cp workout_tracker/workouts.db backup/workouts_backup_20251123.db
```

**Method 2**: Export to CSV (use Export All Data)

### Restore Data

```bash
cp backup/workouts_backup_20251123.db workout_tracker/workouts.db
```

---

## Keyboard Shortcuts

### Global
- **Tab**: Move to next field
- **Shift+Tab**: Move to previous field
- **Enter**: Activate focused button

### Log Workout Tab
- After adding exercise, press **Tab** to move to Reps
- After entering all fields, press **Enter** on "Add Set" button

### History Tab
- **Double-click**: Open workout details
- **Delete**: Select workout, press "Delete Workout"

---

## Best Practices

### Consistent Logging
- Log workouts immediately after finishing
- Use consistent exercise names (e.g., always "Bench Press", not "Bench" or "BP")
- Add notes for context (how you felt, modifications, etc.)

### Data Management
- Export data monthly as backup
- Review analytics weekly to track progress
- Delete test/incorrect workouts promptly

### Performance
- Close app when not in use to save resources
- Export and archive old data if database gets very large (1000+ workouts)

---

## Getting Help

### Documentation
- **README.md**: Project overview
- **QUICKSTART.md**: 5-minute setup
- **FEATURES.md**: Complete feature list
- **BUILD.md**: Build and test instructions
- **PROJECT_COMPLETE.md**: Project summary

### Common Questions

**Q: Can I use this on multiple computers?**
A: Yes, copy the entire folder or just copy `workouts.db` between computers.

**Q: Is my data private?**
A: Yes, all data is stored locally in `workouts.db`. Nothing is sent online.

**Q: Can I import data from other apps?**
A: You can manually insert data into the SQLite database or import CSV data using Python scripts.

**Q: What happens if I lose my database?**
A: Your data is lost unless you have a backup. Export regularly!

**Q: Can I track multiple people's workouts?**
A: Not in the current version. Each database is for one person. You could create multiple database files though.

---

## Project Information

**Version**: 1.0.0
**License**: MIT
**Language**: Python 3.8+
**Platform**: Cross-platform (Windows, macOS, Linux)
**Status**: Production Ready

**Repository Structure**:
```
workout_tracker/
├── workout_tracker/     # Main application code
├── tests/              # Unit tests
├── archive/            # Planning documents
├── README.md           # Main documentation
├── QUICKSTART.md       # Quick start guide
├── FEATURES.md         # Feature list
├── BUILD.md            # Build instructions
├── OPERATION_GUIDE.md  # This file
└── LICENSE             # MIT License
```

---

## Final Checklist

Before running the application, verify:

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install -r workout_tracker/requirements.txt`)
- [ ] In correct directory (project root)
- [ ] Database has write permissions
- [ ] No other instances running

To launch:
```bash
python -m workout_tracker.main
```

---

**Happy tracking! 💪**

For issues or questions, refer to the troubleshooting section or review the comprehensive documentation in the repository.
