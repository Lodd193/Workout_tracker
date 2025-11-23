# Workout Tracker

A modern, feature-rich desktop application for tracking strength training workouts, analyzing progress, and managing fitness data.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-production-brightgreen)

## Features

### 📝 Workout Logging
- **Comprehensive Exercise Tracking**: Log exercises with sets, reps, weight, and RPE (Rate of Perceived Exertion)
- **Cardio Integration**: Track cardio activities with duration and type
- **Smart Set Numbering**: Automatic set numbering per exercise
- **Notes Support**: Add workout notes for each session
- **Date Selection**: Log workouts for any date
- **Workout Types**: Categorize workouts (Push, Pull, Legs, Full Body, etc.)

### 📊 History & Analytics
- **Workout History**: View all past workouts with summary statistics
- **Advanced Filtering**: Filter by date range and workout type
- **Detailed View**: Double-click any workout to see complete details
- **Summary Statistics**: Total workouts, volume, and cardio minutes
- **Delete Functionality**: Remove workouts with confirmation

### 📈 Progress Tracking
- **Lift Progression Charts**: Interactive line charts showing max weight or total volume over time
- **Weekly Volume Analysis**: Bar charts displaying training volume trends (4-24 weeks)
- **Cardio Goal Tracker**: Visual progress indicator for 150 min/week goal
- **Personal Records**: Track max lifts for all exercises
- **Exercise Selector**: View progression for any logged exercise

### 💾 Data Export
- **CSV Export**: Export all data to CSV files for backup or analysis
- **Exercise-Specific Export**: Export data for individual exercises
- **Timestamped Files**: Automatic file naming to prevent overwrites
- **Multiple Formats**: Separate exports for workouts, sets, and cardio

## Screenshots

### Log Workout Tab
Track your exercises, sets, and cardio with an intuitive interface.

### History Tab
View and filter your workout history with detailed information.

### Analytics Tab
Visualize your progress with interactive charts and statistics.

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/workout-tracker.git
   cd workout-tracker
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r workout_tracker/requirements.txt
   ```

4. **Run the application**
   ```bash
   python -m workout_tracker.main
   ```

## Dependencies

- **ttkbootstrap** - Modern themed tkinter widgets
- **matplotlib** - Interactive charts and visualizations
- **pandas** - Data analysis and manipulation
- **python-dateutil** - Date/time utilities

All dependencies are listed in `workout_tracker/requirements.txt`.

## Usage Guide

### Logging a Workout

1. Navigate to the **Log Workout** tab
2. Select the date and workout type
3. Enter exercise details:
   - Exercise name
   - Reps
   - Weight (lbs)
   - RPE (optional, 0-10 scale)
4. Click **Add Set** to add the set to your workout
5. Repeat for all exercises
6. (Optional) Add cardio minutes and type
7. (Optional) Add workout notes
8. Click **Save Workout**

### Viewing History

1. Navigate to the **History** tab
2. Use filters to narrow results:
   - Date range (From/To)
   - Workout type
3. Click **Apply Filters** to update the view
4. Double-click any workout to see full details
5. Select and click **Delete Workout** to remove (with confirmation)

### Analyzing Progress

1. Navigate to the **Analytics** tab
2. **Lift Progression**:
   - Select an exercise from the dropdown
   - Choose chart type (Max Weight or Total Volume)
   - Use toolbar to zoom/pan
3. **Weekly Volume**:
   - Adjust time range (4-24 weeks)
   - Click **Update** to refresh
4. **Cardio Goal**:
   - View current week progress toward 150 min goal
   - Click **Refresh** to update
5. **Export Data**:
   - Click **Export All Data** to save all workout data
   - Click **Export Exercise** to save current exercise data

## Project Structure

```
workout_tracker/
├── workout_tracker/
│   ├── __init__.py           # Package initialization
│   ├── main.py               # Application entry point
│   ├── db.py                 # Database layer (SQLite)
│   ├── export.py             # CSV export functionality
│   ├── requirements.txt      # Python dependencies
│   ├── workouts.db           # SQLite database (created on first run)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── workout_service.py    # Workout CRUD operations
│   │   └── analytics_service.py  # Analytics and statistics
│   └── ui/
│       ├── __init__.py
│       ├── main_window.py        # Main window with tabs
│       ├── log_workout_view.py   # Log workout interface
│       ├── history_view.py       # History viewer
│       └── analytics_view.py     # Charts and analytics
├── .gitignore
└── README.md
```

## Database Schema

### Workouts Table
- `id`: Primary key
- `date`: Workout date (YYYY-MM-DD)
- `workout_type`: Type of workout (Push, Pull, etc.)
- `notes`: Optional workout notes

### Sets Table
- `id`: Primary key
- `workout_id`: Foreign key to workouts
- `exercise_name`: Name of the exercise
- `set_number`: Set number for this exercise
- `reps`: Number of repetitions
- `weight`: Weight lifted (lbs)
- `rpe`: Rate of Perceived Exertion (0-10)

### Cardio Sessions Table
- `id`: Primary key
- `workout_id`: Foreign key to workouts
- `cardio_type`: Type of cardio activity
- `minutes`: Duration in minutes

## Technical Highlights

### Architecture
- **MVC Pattern**: Separation of data (db.py), business logic (services/), and UI (ui/)
- **SQLite Database**: Lightweight, file-based database with proper schema design
- **Service Layer**: Clean abstraction between UI and database operations
- **Modular Design**: Each tab is a separate view component

### Key Features
- **Data Validation**: Input validation with user-friendly error messages
- **Error Handling**: Comprehensive exception handling throughout
- **User Feedback**: Success/error dialogs for all operations
- **Responsive UI**: Proper use of frames, padding, and layouts
- **Interactive Charts**: Matplotlib integration with zoom/pan toolbars

### Code Quality
- **Type Hints**: Clear function signatures (where applicable)
- **Docstrings**: Comprehensive documentation for all modules and functions
- **Comments**: Inline comments for complex logic
- **Consistent Style**: PEP 8 compliant code formatting

## Future Enhancements (Phase 10 - Optional)

Potential improvements for portfolio expansion:

- [ ] **Plotly Dashboard**: Generate interactive HTML reports
- [ ] **PyInstaller Build**: Create standalone .exe for Windows
- [ ] **Unit Tests**: Add pytest test coverage
- [ ] **1RM Calculator**: Display estimated one-rep max
- [ ] **Body Weight Tracking**: Track body weight over time
- [ ] **Exercise Library**: Pre-populated exercise database
- [ ] **Custom Themes**: Additional ttkbootstrap themes
- [ ] **Cloud Sync**: Backup data to cloud storage
- [ ] **Mobile Export**: QR code for data transfer

## Contributing

This is a portfolio project, but feedback and suggestions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -m 'Add improvement'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2025 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Acknowledgments

- Built with [ttkbootstrap](https://ttkbootstrap.readthedocs.io/) for modern UI components
- Charts powered by [matplotlib](https://matplotlib.org/)
- Data analysis using [pandas](https://pandas.pydata.org/)

## Contact

For questions or feedback:
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

---

**Note**: This is a portfolio project demonstrating Python GUI development, database design, data visualization, and software engineering best practices.
