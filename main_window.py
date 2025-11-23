# workout_tracker/ui/main_window.py

from ttkbootstrap import Frame, Notebook
from ttkbootstrap.constants import *
from .log_workout_view import LogWorkoutView
from .history_view import HistoryView
from .analytics_view import AnalyticsView


class MainWindow(Frame):
    """Main application frame containing the tabbed interface."""

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        # Make this frame fill the window
        self.pack(fill=BOTH, expand=YES)
        self._build_ui()

    def _build_ui(self):
        """Create the Notebook (tabs) and add the tab views."""
        notebook = Notebook(self)
        notebook.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        # Create tab frames
        log_tab = LogWorkoutView(notebook)
        history_tab = HistoryView(notebook)
        analytics_tab = AnalyticsView(notebook)

        # Add tabs to the notebook
        notebook.add(log_tab, text="Log Workout")
        notebook.add(history_tab, text="History")
        notebook.add(analytics_tab, text="Analytics")
