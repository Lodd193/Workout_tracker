from ttkbootstrap import Window
from ttkbootstrap.constants import *
from pathlib import Path
from .ui.main_window import MainWindow
from .db import create_tables


def main():
    # Create DB on startup if needed
    create_tables()

    # Create the main application window
    app = Window(themename="superhero")
    app.title("Workout Tracker")
    app.geometry("1600x1000")  # Large window size to display all UI elements comfortably

    # Make window resizable and set minimum size
    app.minsize(1200, 800)

    # Set custom icon
    icon_path = Path(__file__).parent.parent / "workout_tracker.ico"
    if icon_path.exists():
        app.iconbitmap(str(icon_path))

    MainWindow(app)

    app.mainloop()


if __name__ == "__main__":
    main()
