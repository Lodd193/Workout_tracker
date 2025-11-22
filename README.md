Workout Tracker – Desktop App (Python, Tkinter, Matplotlib)
A modern, easy-to-use desktop workout tracker built with Python, ttkbootstrap, SQLite, and Matplotlib.
Designed for personal use and as a polished portfolio project showcasing:
•	GUI development
•	Data modelling
•	Analytics with pandas
•	Embedded Matplotlib charts
•	Clean software architecture
•	Exportable fitness data
This app helps you log strength workouts, track cardio minutes, and visualise your progress in a simple, modern interface.
________________________________________
✨ Features
🏋️ Log Strength Workouts
•	Add exercises with:
o	Sets
o	Reps
o	Weight
o	RPE
•	Add optional notes
•	Automatically compute session totals (e.g., volume = reps × weight)

❤️ Track Weekly Cardio Goal
•	Simple entry for cardio minutes per workout
•	Weekly goal: 150 minutes (visual indicator included)

📅 Workout History
•	View all workouts in a sortable table
•	See:
o	Date
o	Workout type
o	Total sets
o	Total volume
o	Cardio minutes
•	Filter by date range or workout type
•	View full details of each workout

📈 Progress & Analytics
Powered by Matplotlib + pandas:
•	Lift progression graphs
o	Track performance for any exercise
o	View top set weight or estimated 1RM
o	Fully interactive via Matplotlib toolbar (zoom, pan, save)
•	Weekly training volume
o	Bar chart of total weekly volume (Σ reps × weight)
o	Great for monitoring training load over time
•	Cardio goal indicator
o	Shows weekly minutes achieved out of 150
o	Highlights when goal is reached

📤 Export Data
Export your fitness data into CSV for use in:
•	Excel
•	Google Sheets
•	Python notebooks
•	BI dashboards
Exports include:
•	workouts.csv
•	sets.csv
•	cardio_sessions.csv
________________________________________
🛠 Tech Stack
•	Python 3.10+
•	Tkinter + ttkbootstrap (modern UI styling)
•	SQLite for local persistent storage
•	pandas for analytics and aggregation
•	Matplotlib (embedded via FigureCanvasTkAgg)
•	Optional: PyInstaller for building a standalone .exe on Windows

workout_tracker/
├── workout_tracker/
│   ├── main.py                 # Launches the GUI and tabs
│   ├── db.py                   # Handles SQLite connection + schema
│   ├── models.py               # Dataclasses (optional)
│   ├── services/
│   │   ├── workout_service.py      # CRUD for workouts/sets/cardio
│   │   └── analytics_service.py    # Progress calculations
│   ├── ui/
│   │   ├── main_window.py          # ttkbootstrap root + Notebook
│   │   ├── log_workout_view.py     # Workout logging tab
│   │   ├── history_view.py         # Workout history tab
│   │   └── analytics_view.py       # Charts + analytics tab
│   └── export.py               # CSV export functions
├── requirements.txt
└── README.md


🧩 Future Enhancements (Roadmap)
•	Editable exercise library (add/remove custom exercises)
•	Tags for workouts (e.g., “Upper A”, “Cardio”, “Hypertrophy”)
•	PR tracking (auto-detect new personal bests)
•	Automatic 1RM calculation per workout
•	Export directly to Excel
•	Optional Plotly dashboard as a separate module

