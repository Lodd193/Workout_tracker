# workout_tracker/ui/analytics_view.py

from datetime import datetime
from tkinter import filedialog
import os
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator

from ..services.analytics_service import (
    get_exercise_progression,
    get_top_set_by_date,
    get_weekly_volume,
    get_current_week_cardio,
    get_personal_records
)
from ..services.workout_service import get_exercises
from ..export import export_all_data, export_exercise_data


class AnalyticsView(tb.Frame):
    """Tab for viewing analytics and progress charts."""

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.current_exercise = None
        self._build_ui()
        self._load_initial_data()

    def _build_ui(self):
        """Build the complete Analytics interface."""

        # Main container with padding
        container = tb.Frame(self, padding=20)
        container.pack(fill=BOTH, expand=YES)

        # Title
        title = tb.Label(
            container,
            text="Analytics & Progress",
            font=("Helvetica", 18, "bold"),
            bootstyle="inverse-primary"
        )
        title.pack(pady=(0, 20))

        # ===== CARDIO GOAL SECTION =====
        cardio_frame = tb.Labelframe(container, text="Cardio Goal (This Week)", padding=15)
        cardio_frame.pack(fill=X, pady=(0, 15))

        cardio_container = tb.Frame(cardio_frame)
        cardio_container.pack(fill=X)

        # Cardio stats
        self.cardio_label = tb.Label(
            cardio_container,
            text="Loading...",
            font=("Helvetica", 14, "bold")
        )
        self.cardio_label.pack(side=LEFT, padx=(0, 20))

        # Progress bar
        self.cardio_progress = tb.Progressbar(
            cardio_container,
            mode='determinate',
            bootstyle="success",
            length=300
        )
        self.cardio_progress.pack(side=LEFT, fill=X, expand=YES, padx=(0, 20))

        # Refresh cardio button
        refresh_cardio_btn = tb.Button(
            cardio_container,
            text="Refresh",
            bootstyle="info",
            command=self._update_cardio_goal,
            width=10
        )
        refresh_cardio_btn.pack(side=LEFT)

        # ===== CHARTS SECTION =====
        charts_container = tb.Frame(container)
        charts_container.pack(fill=BOTH, expand=YES)

        # Left side: Lift Progression
        left_frame = tb.Labelframe(charts_container, text="Lift Progression", padding=10)
        left_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 10))

        # Exercise selector
        selector_frame = tb.Frame(left_frame)
        selector_frame.pack(fill=X, pady=(0, 10))

        tb.Label(selector_frame, text="Select Exercise:", width=15).pack(side=LEFT)
        self.exercise_var = tb.StringVar()
        self.exercise_combo = tb.Combobox(
            selector_frame,
            textvariable=self.exercise_var,
            state="readonly",
            width=25
        )
        self.exercise_combo.pack(side=LEFT, padx=(5, 10), fill=X, expand=YES)
        self.exercise_combo.bind("<<ComboboxSelected>>", self._on_exercise_selected)

        update_lift_btn = tb.Button(
            selector_frame,
            text="Update",
            bootstyle="primary",
            command=self._update_lift_chart,
            width=10
        )
        update_lift_btn.pack(side=LEFT)

        # Chart type selector
        chart_type_frame = tb.Frame(left_frame)
        chart_type_frame.pack(fill=X, pady=(0, 10))

        tb.Label(chart_type_frame, text="Chart Type:", width=15).pack(side=LEFT)
        self.chart_type_var = tb.StringVar(value="Max Weight")
        chart_type_radio1 = tb.Radiobutton(
            chart_type_frame,
            text="Max Weight",
            variable=self.chart_type_var,
            value="Max Weight",
            bootstyle="primary"
        )
        chart_type_radio1.pack(side=LEFT, padx=5)

        chart_type_radio2 = tb.Radiobutton(
            chart_type_frame,
            text="Total Volume",
            variable=self.chart_type_var,
            value="Total Volume",
            bootstyle="primary"
        )
        chart_type_radio2.pack(side=LEFT, padx=5)

        # Lift progression chart
        self.lift_fig = Figure(figsize=(6, 4), dpi=100)
        self.lift_ax = self.lift_fig.add_subplot(111)
        self.lift_canvas = FigureCanvasTkAgg(self.lift_fig, left_frame)
        self.lift_canvas.get_tk_widget().pack(fill=BOTH, expand=YES)

        # Toolbar for lift chart
        lift_toolbar_frame = tb.Frame(left_frame)
        lift_toolbar_frame.pack(fill=X)
        self.lift_toolbar = NavigationToolbar2Tk(self.lift_canvas, lift_toolbar_frame)
        self.lift_toolbar.update()

        # Right side: Weekly Volume
        right_frame = tb.Labelframe(charts_container, text="Weekly Volume (Last 12 Weeks)", padding=10)
        right_frame.pack(side=LEFT, fill=BOTH, expand=YES)

        # Volume controls
        volume_controls = tb.Frame(right_frame)
        volume_controls.pack(fill=X, pady=(0, 10))

        tb.Label(volume_controls, text="Weeks:", width=10).pack(side=LEFT)
        self.weeks_var = tb.StringVar(value="12")
        weeks_spinbox = tb.Spinbox(
            volume_controls,
            from_=4,
            to=24,
            textvariable=self.weeks_var,
            width=8,
            state="readonly"
        )
        weeks_spinbox.pack(side=LEFT, padx=(5, 10))

        update_volume_btn = tb.Button(
            volume_controls,
            text="Update",
            bootstyle="primary",
            command=self._update_volume_chart,
            width=10
        )
        update_volume_btn.pack(side=LEFT)

        # Weekly volume chart
        self.volume_fig = Figure(figsize=(6, 4), dpi=100)
        self.volume_ax = self.volume_fig.add_subplot(111)
        self.volume_canvas = FigureCanvasTkAgg(self.volume_fig, right_frame)
        self.volume_canvas.get_tk_widget().pack(fill=BOTH, expand=YES)

        # Toolbar for volume chart
        volume_toolbar_frame = tb.Frame(right_frame)
        volume_toolbar_frame.pack(fill=X)
        self.volume_toolbar = NavigationToolbar2Tk(self.volume_canvas, volume_toolbar_frame)
        self.volume_toolbar.update()

        # ===== PERSONAL RECORDS SECTION =====
        pr_frame = tb.Labelframe(container, text="Personal Records", padding=15)
        pr_frame.pack(fill=X, pady=(15, 0))

        self.pr_label = tb.Label(
            pr_frame,
            text="Click 'Refresh PRs' to view your personal records",
            font=("Helvetica", 10)
        )
        self.pr_label.pack(side=LEFT, fill=X, expand=YES)

        refresh_pr_btn = tb.Button(
            pr_frame,
            text="Refresh PRs",
            bootstyle="success",
            command=self._update_personal_records,
            width=15
        )
        refresh_pr_btn.pack(side=LEFT)

        # ===== EXPORT SECTION =====
        export_frame = tb.Labelframe(container, text="Export Data", padding=15)
        export_frame.pack(fill=X, pady=(15, 0))

        export_info = tb.Label(
            export_frame,
            text="Export your workout data to CSV files for backup or analysis",
            font=("Helvetica", 10, "italic")
        )
        export_info.pack(side=LEFT, fill=X, expand=YES)

        export_all_btn = tb.Button(
            export_frame,
            text="Export All Data",
            bootstyle="primary",
            command=self._export_all,
            width=18
        )
        export_all_btn.pack(side=LEFT, padx=5)

        export_exercise_btn = tb.Button(
            export_frame,
            text="Export Exercise",
            bootstyle="info",
            command=self._export_current_exercise,
            width=18
        )
        export_exercise_btn.pack(side=LEFT, padx=5)

    def _load_initial_data(self):
        """Load initial data when the view is created."""
        self._update_cardio_goal()
        self._load_exercises()
        self._update_volume_chart()
        self._update_personal_records()

    def _load_exercises(self):
        """Load available exercises into the dropdown."""
        try:
            exercises = get_exercises()
            if exercises:
                self.exercise_combo['values'] = exercises
                self.exercise_combo.current(0)
                self.current_exercise = exercises[0]
                self._update_lift_chart()
            else:
                self.exercise_combo['values'] = ["No exercises found"]
                self._show_empty_lift_chart()
        except Exception as e:
            Messagebox.show_error(f"Error loading exercises:\n{str(e)}", "Error")

    def _on_exercise_selected(self, event):
        """Handle exercise selection change."""
        self.current_exercise = self.exercise_var.get()
        self._update_lift_chart()

    def _update_cardio_goal(self):
        """Update the cardio goal progress indicator."""
        try:
            current_minutes = get_current_week_cardio()
            goal = 150

            # Update label
            if current_minutes >= goal:
                self.cardio_label.config(
                    text=f"Goal Reached! {current_minutes}/{goal} mins",
                    bootstyle="success"
                )
            else:
                remaining = goal - current_minutes
                self.cardio_label.config(
                    text=f"{current_minutes}/{goal} mins ({remaining} to go)",
                    bootstyle="info"
                )

            # Update progress bar
            progress_percent = min((current_minutes / goal) * 100, 100)
            self.cardio_progress['value'] = progress_percent

            # Change progress bar color based on completion
            if progress_percent >= 100:
                self.cardio_progress.config(bootstyle="success")
            elif progress_percent >= 50:
                self.cardio_progress.config(bootstyle="warning")
            else:
                self.cardio_progress.config(bootstyle="info")

        except Exception as e:
            self.cardio_label.config(text=f"Error: {str(e)}")

    def _update_lift_chart(self):
        """Update the lift progression chart for the selected exercise."""
        if not self.current_exercise or self.current_exercise == "No exercises found":
            self._show_empty_lift_chart()
            return

        try:
            # Get data
            progression_data = get_top_set_by_date(self.current_exercise)

            if not progression_data:
                self._show_empty_lift_chart()
                return

            chart_type = self.chart_type_var.get()

            # Clear previous plot
            self.lift_ax.clear()

            if chart_type == "Max Weight":
                # Sort data by date chronologically
                sorted_data = sorted(progression_data, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))
                dates = [datetime.strptime(d['date'], '%Y-%m-%d') for d in sorted_data]
                weights = [d['weight'] for d in sorted_data]
                self.lift_ax.plot(dates, weights, marker='o', linestyle='-', linewidth=2, markersize=6, color='#3498db')
                self.lift_ax.set_ylabel('Weight (lbs)', fontsize=10)
                self.lift_ax.set_title(f'{self.current_exercise} - Max Weight Progression', fontsize=12, fontweight='bold')
            else:  # Total Volume
                # Get full progression data for volume
                full_data = get_exercise_progression(self.current_exercise)
                # Sort data by date chronologically
                sorted_data = sorted(full_data, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))
                dates = [datetime.strptime(d['date'], '%Y-%m-%d') for d in sorted_data]
                volumes = [d['total_volume'] for d in sorted_data]
                self.lift_ax.plot(dates, volumes, marker='o', linestyle='-', linewidth=2, markersize=6, color='#2ecc71')
                self.lift_ax.set_ylabel('Volume (lbs)', fontsize=10)
                self.lift_ax.set_title(f'{self.current_exercise} - Volume Progression', fontsize=12, fontweight='bold')

            # Format x-axis with automatic spacing
            self.lift_ax.set_xlabel('Date', fontsize=10)
            self.lift_fig.autofmt_xdate()
            self.lift_ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))  # Show as "Jan 15"
            # Limit to reasonable number of ticks
            self.lift_ax.xaxis.set_major_locator(MaxNLocator(8))
            self.lift_ax.grid(True, alpha=0.3)
            self.lift_fig.tight_layout()

            # Refresh canvas
            self.lift_canvas.draw()

        except Exception as e:
            Messagebox.show_error(f"Error updating lift chart:\n{str(e)}", "Chart Error")

    def _show_empty_lift_chart(self):
        """Show an empty state for the lift chart."""
        self.lift_ax.clear()
        self.lift_ax.text(
            0.5, 0.5,
            'No data available\nLog workouts to see progression',
            horizontalalignment='center',
            verticalalignment='center',
            transform=self.lift_ax.transAxes,
            fontsize=12,
            color='gray'
        )
        self.lift_ax.set_xticks([])
        self.lift_ax.set_yticks([])
        self.lift_canvas.draw()

    def _update_volume_chart(self):
        """Update the weekly volume bar chart."""
        try:
            weeks = int(self.weeks_var.get())
            volume_data = get_weekly_volume(weeks)

            # Clear previous plot
            self.volume_ax.clear()

            if not volume_data:
                self.volume_ax.text(
                    0.5, 0.5,
                    'No data available\nLog workouts to see volume',
                    horizontalalignment='center',
                    verticalalignment='center',
                    transform=self.volume_ax.transAxes,
                    fontsize=12,
                    color='gray'
                )
                self.volume_ax.set_xticks([])
                self.volume_ax.set_yticks([])
                self.volume_canvas.draw()
                return

            # Sort data by week_start chronologically
            sorted_data = sorted(volume_data, key=lambda x: datetime.strptime(x['week_start'], '%Y-%m-%d'))

            # Extract data
            week_starts = [datetime.strptime(d['week_start'], '%Y-%m-%d') for d in sorted_data]
            volumes = [d['total_volume'] or 0 for d in sorted_data]

            # Create bar chart
            bars = self.volume_ax.bar(week_starts, volumes, width=5, color='#9b59b6', alpha=0.8)

            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    self.volume_ax.text(
                        bar.get_x() + bar.get_width() / 2.,
                        height,
                        f'{int(height):,}',
                        ha='center',
                        va='bottom',
                        fontsize=8
                    )

            # Format chart
            self.volume_ax.set_xlabel('Week Starting', fontsize=10)
            self.volume_ax.set_ylabel('Total Volume (lbs)', fontsize=10)
            self.volume_ax.set_title(f'Weekly Training Volume (Last {weeks} Weeks)', fontsize=12, fontweight='bold')
            self.volume_fig.autofmt_xdate()
            self.volume_ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))  # Show as "Jan 15"
            # Limit number of x-axis labels for readability
            self.volume_ax.xaxis.set_major_locator(MaxNLocator(6))
            self.volume_ax.grid(True, alpha=0.3, axis='y')
            self.volume_fig.tight_layout()

            # Refresh canvas
            self.volume_canvas.draw()

        except Exception as e:
            Messagebox.show_error(f"Error updating volume chart:\n{str(e)}", "Chart Error")

    def _update_personal_records(self):
        """Update the personal records display."""
        try:
            prs = get_personal_records()

            if not prs:
                self.pr_label.config(text="No personal records yet. Start logging workouts!")
                return

            # Format PRs for display
            pr_text = "Personal Records: "
            pr_list = []
            for pr in prs[:5]:  # Show top 5
                pr_list.append(f"{pr['exercise_name']}: {pr['max_weight']} lbs")

            if len(prs) > 5:
                pr_text += ", ".join(pr_list) + f" ... and {len(prs) - 5} more"
            else:
                pr_text += ", ".join(pr_list)

            self.pr_label.config(text=pr_text)

        except Exception as e:
            self.pr_label.config(text=f"Error loading PRs: {str(e)}")

    def _export_all(self):
        """Export all workout data to CSV files."""
        # Ask user to select directory
        directory = filedialog.askdirectory(
            title="Select Export Directory",
            initialdir=os.path.expanduser("~")
        )

        if not directory:
            return  # User cancelled

        try:
            # Export all data
            result = export_all_data(directory)

            # Show success message
            message = (
                f"Export successful!\n\n"
                f"Workouts: {result['workouts']}\n"
                f"Sets: {result['sets']}\n"
                f"Cardio Sessions: {result['cardio']}\n\n"
                f"Files saved to:\n{directory}"
            )

            Messagebox.show_info(message, "Export Complete")

        except Exception as e:
            Messagebox.show_error(
                f"Error exporting data:\n{str(e)}",
                "Export Error"
            )

    def _export_current_exercise(self):
        """Export data for the currently selected exercise."""
        if not self.current_exercise or self.current_exercise == "No exercises found":
            Messagebox.show_warning(
                "Please select an exercise first.",
                "No Exercise Selected"
            )
            return

        # Ask user for save location
        filename = filedialog.asksaveasfilename(
            title="Save Exercise Data",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"{self.current_exercise.replace(' ', '_')}_data.csv"
        )

        if not filename:
            return  # User cancelled

        try:
            # Export exercise data
            count = export_exercise_data(self.current_exercise, filename)

            # Show success message
            Messagebox.show_info(
                f"Successfully exported {count} sets for {self.current_exercise}.\n\n"
                f"File saved to:\n{filename}",
                "Export Complete"
            )

        except Exception as e:
            Messagebox.show_error(
                f"Error exporting exercise data:\n{str(e)}",
                "Export Error"
            )
