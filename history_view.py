# workout_tracker/ui/history_view.py

from datetime import datetime, timedelta
from tkinter import ttk, Toplevel, Text
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from ..services.workout_service import (
    get_workouts,
    get_workout_details,
    delete_workout,
    get_workout_types
)


class HistoryView(tb.Frame):
    """Tab for viewing and filtering workout history."""

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.current_workouts = []  # Store current filtered workouts
        self._build_ui()
        self._load_workouts()  # Load initial data

    def _build_ui(self):
        """Build the complete History interface."""

        # Main container with padding
        container = tb.Frame(self, padding=20)
        container.pack(fill=BOTH, expand=YES)

        # Title
        title = tb.Label(
            container,
            text="Workout History",
            font=("Helvetica", 18, "bold"),
            bootstyle="inverse-primary"
        )
        title.pack(pady=(0, 20))

        # ===== FILTER SECTION =====
        filter_frame = tb.Labelframe(container, text="Filters", padding=15)
        filter_frame.pack(fill=X, pady=(0, 15))

        # Date range filter
        date_row = tb.Frame(filter_frame)
        date_row.pack(fill=X, pady=5)

        tb.Label(date_row, text="Date Range:", width=15).pack(side=LEFT)

        tb.Label(date_row, text="From:").pack(side=LEFT, padx=(10, 5))
        self.start_date_entry = tb.DateEntry(date_row, dateformat="%Y-%m-%d", width=12)
        self.start_date_entry.pack(side=LEFT, padx=(0, 15))

        # Set default to 30 days ago
        default_start = datetime.now() - timedelta(days=30)
        self.start_date_entry.entry.delete(0, END)
        self.start_date_entry.entry.insert(0, default_start.strftime("%Y-%m-%d"))

        tb.Label(date_row, text="To:").pack(side=LEFT, padx=(0, 5))
        self.end_date_entry = tb.DateEntry(date_row, dateformat="%Y-%m-%d", width=12)
        self.end_date_entry.pack(side=LEFT)

        # Workout type filter
        type_row = tb.Frame(filter_frame)
        type_row.pack(fill=X, pady=5)

        tb.Label(type_row, text="Workout Type:", width=15).pack(side=LEFT)
        self.filter_type_var = tb.StringVar(value="All")
        self.filter_type_combo = tb.Combobox(
            type_row,
            textvariable=self.filter_type_var,
            values=["All"],
            state="readonly",
            width=20
        )
        self.filter_type_combo.pack(side=LEFT, padx=(10, 20))

        # Filter buttons
        filter_btn = tb.Button(
            type_row,
            text="Apply Filters",
            bootstyle="primary",
            command=self._apply_filters
        )
        filter_btn.pack(side=LEFT, padx=5)

        clear_filter_btn = tb.Button(
            type_row,
            text="Clear Filters",
            bootstyle="secondary",
            command=self._clear_filters
        )
        clear_filter_btn.pack(side=LEFT, padx=5)

        refresh_btn = tb.Button(
            type_row,
            text="Refresh",
            bootstyle="info",
            command=self._load_workouts
        )
        refresh_btn.pack(side=LEFT, padx=5)

        # ===== WORKOUTS TABLE =====
        table_frame = tb.Labelframe(container, text="Workouts", padding=15)
        table_frame.pack(fill=BOTH, expand=YES, pady=(0, 15))

        # Treeview container with scrollbar
        tree_container = tb.Frame(table_frame)
        tree_container.pack(fill=BOTH, expand=YES)

        # Scrollbars
        vsb = tb.Scrollbar(tree_container, orient=VERTICAL)
        vsb.pack(side=RIGHT, fill=Y)

        hsb = tb.Scrollbar(tree_container, orient=HORIZONTAL)
        hsb.pack(side=BOTTOM, fill=X)

        # Treeview
        self.workouts_tree = ttk.Treeview(
            tree_container,
            columns=("date", "type", "sets", "volume", "cardio", "id"),
            show="headings",
            height=12,
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )
        vsb.config(command=self.workouts_tree.yview)
        hsb.config(command=self.workouts_tree.xview)

        # Define columns
        self.workouts_tree.heading("date", text="Date")
        self.workouts_tree.heading("type", text="Workout Type")
        self.workouts_tree.heading("sets", text="Total Sets")
        self.workouts_tree.heading("volume", text="Total Volume (lbs)")
        self.workouts_tree.heading("cardio", text="Cardio (mins)")
        self.workouts_tree.heading("id", text="ID")

        self.workouts_tree.column("date", width=120, anchor=W)
        self.workouts_tree.column("type", width=150, anchor=W)
        self.workouts_tree.column("sets", width=100, anchor=CENTER)
        self.workouts_tree.column("volume", width=150, anchor=CENTER)
        self.workouts_tree.column("cardio", width=120, anchor=CENTER)
        self.workouts_tree.column("id", width=60, anchor=CENTER)

        self.workouts_tree.pack(fill=BOTH, expand=YES)

        # Double-click to view details
        self.workouts_tree.bind("<Double-Button-1>", self._on_double_click)

        # Summary label
        self.summary_label = tb.Label(
            table_frame,
            text="Total workouts: 0",
            font=("Helvetica", 10, "italic")
        )
        self.summary_label.pack(pady=(10, 0))

        # ===== ACTION BUTTONS =====
        button_frame = tb.Frame(container)
        button_frame.pack(fill=X)

        view_btn = tb.Button(
            button_frame,
            text="View Details",
            bootstyle="info",
            command=self._view_details,
            width=15
        )
        view_btn.pack(side=LEFT, padx=(0, 10))

        delete_btn = tb.Button(
            button_frame,
            text="Delete Workout",
            bootstyle="danger",
            command=self._delete_workout,
            width=15
        )
        delete_btn.pack(side=LEFT)

    def _load_workouts(self, start_date=None, end_date=None, workout_type=None):
        """Load workouts from database with optional filters."""
        try:
            # Get workouts
            workouts = get_workouts(start_date, end_date, workout_type)
            self.current_workouts = workouts

            # Clear treeview
            for item in self.workouts_tree.get_children():
                self.workouts_tree.delete(item)

            # Populate treeview
            for workout in workouts:
                self.workouts_tree.insert(
                    "",
                    END,
                    values=(
                        workout['date'],
                        workout['workout_type'],
                        workout['total_sets'] or 0,
                        f"{workout['total_volume']:.1f}" if workout['total_volume'] else "0.0",
                        workout['cardio_minutes'] or 0,
                        workout['id']
                    )
                )

            # Update summary
            total_volume = sum(w['total_volume'] or 0 for w in workouts)
            total_cardio = sum(w['cardio_minutes'] or 0 for w in workouts)
            self.summary_label.config(
                text=f"Total workouts: {len(workouts)} | "
                     f"Total volume: {total_volume:,.1f} lbs | "
                     f"Total cardio: {total_cardio} mins"
            )

            # Update workout type filter options
            self._update_type_filter()

        except Exception as e:
            Messagebox.show_error(
                f"Error loading workouts:\n{str(e)}",
                "Load Error"
            )

    def _update_type_filter(self):
        """Update the workout type filter dropdown with available types."""
        try:
            types = get_workout_types()
            filter_values = ["All"] + types
            self.filter_type_combo['values'] = filter_values
        except Exception as e:
            print(f"Error updating type filter: {e}")

    def _apply_filters(self):
        """Apply the selected filters and reload workouts."""
        start_date = self.start_date_entry.entry.get().strip()
        end_date = self.end_date_entry.entry.get().strip()
        workout_type = self.filter_type_var.get()

        # Convert "All" to None
        if workout_type == "All":
            workout_type = None

        # Validate dates
        if not start_date:
            start_date = None
        if not end_date:
            end_date = None

        self._load_workouts(start_date, end_date, workout_type)

    def _clear_filters(self):
        """Clear all filters and reload all workouts."""
        # Reset date range to last 30 days
        default_start = datetime.now() - timedelta(days=30)
        self.start_date_entry.entry.delete(0, END)
        self.start_date_entry.entry.insert(0, default_start.strftime("%Y-%m-%d"))

        self.end_date_entry.entry.delete(0, END)
        self.end_date_entry.entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Reset type filter
        self.filter_type_var.set("All")

        # Reload all workouts
        self._load_workouts()

    def _get_selected_workout_id(self):
        """Get the ID of the currently selected workout."""
        selected = self.workouts_tree.selection()
        if not selected:
            return None

        item = self.workouts_tree.item(selected[0])
        values = item['values']
        return values[5]  # ID is the 6th column (index 5)

    def _view_details(self):
        """View detailed information about the selected workout."""
        workout_id = self._get_selected_workout_id()
        if not workout_id:
            Messagebox.show_warning("Please select a workout to view.", "No Selection")
            return

        self._show_workout_details(workout_id)

    def _on_double_click(self, event):
        """Handle double-click on a workout row."""
        workout_id = self._get_selected_workout_id()
        if workout_id:
            self._show_workout_details(workout_id)

    def _show_workout_details(self, workout_id):
        """Show a popup with detailed workout information."""
        try:
            details = get_workout_details(workout_id)
            if not details:
                Messagebox.show_error("Workout not found.", "Error")
                return

            # Create popup window
            popup = Toplevel(self)
            popup.title(f"Workout Details - {details['workout']['date']}")
            popup.geometry("700x500")

            # Main frame
            main_frame = tb.Frame(popup, padding=20)
            main_frame.pack(fill=BOTH, expand=YES)

            # Title
            title = tb.Label(
                main_frame,
                text=f"Workout: {details['workout']['workout_type']}",
                font=("Helvetica", 16, "bold")
            )
            title.pack(pady=(0, 10))

            # Date
            date_label = tb.Label(
                main_frame,
                text=f"Date: {details['workout']['date']}",
                font=("Helvetica", 12)
            )
            date_label.pack(pady=(0, 20))

            # Sets section
            if details['sets']:
                sets_label = tb.Label(
                    main_frame,
                    text="Exercises & Sets:",
                    font=("Helvetica", 12, "bold")
                )
                sets_label.pack(anchor=W, pady=(0, 10))

                # Create sets table
                sets_frame = tb.Frame(main_frame)
                sets_frame.pack(fill=BOTH, expand=YES, pady=(0, 20))

                sets_tree = ttk.Treeview(
                    sets_frame,
                    columns=("exercise", "set", "reps", "weight", "rpe"),
                    show="headings",
                    height=10
                )

                sets_tree.heading("exercise", text="Exercise")
                sets_tree.heading("set", text="Set #")
                sets_tree.heading("reps", text="Reps")
                sets_tree.heading("weight", text="Weight (lbs)")
                sets_tree.heading("rpe", text="RPE")

                sets_tree.column("exercise", width=200)
                sets_tree.column("set", width=80, anchor=CENTER)
                sets_tree.column("reps", width=80, anchor=CENTER)
                sets_tree.column("weight", width=120, anchor=CENTER)
                sets_tree.column("rpe", width=80, anchor=CENTER)

                for s in details['sets']:
                    sets_tree.insert(
                        "",
                        END,
                        values=(
                            s['exercise_name'],
                            s['set_number'],
                            s['reps'],
                            s['weight'],
                            s['rpe'] if s['rpe'] else "-"
                        )
                    )

                sets_tree.pack(fill=BOTH, expand=YES)

            # Cardio section
            if details['cardio']:
                cardio_label = tb.Label(
                    main_frame,
                    text="Cardio:",
                    font=("Helvetica", 12, "bold")
                )
                cardio_label.pack(anchor=W, pady=(10, 5))

                for c in details['cardio']:
                    cardio_info = tb.Label(
                        main_frame,
                        text=f"  {c['cardio_type']}: {c['minutes']} minutes"
                    )
                    cardio_info.pack(anchor=W)

            # Notes section
            if details['workout'].get('notes'):
                notes_label = tb.Label(
                    main_frame,
                    text="Notes:",
                    font=("Helvetica", 12, "bold")
                )
                notes_label.pack(anchor=W, pady=(10, 5))

                notes_text = Text(main_frame, height=4, width=60, wrap="word")
                notes_text.insert("1.0", details['workout']['notes'])
                notes_text.config(state="disabled")
                notes_text.pack(fill=X, pady=(0, 10))

            # Close button
            close_btn = tb.Button(
                main_frame,
                text="Close",
                bootstyle="secondary",
                command=popup.destroy,
                width=15
            )
            close_btn.pack(pady=(10, 0))

        except Exception as e:
            Messagebox.show_error(
                f"Error loading workout details:\n{str(e)}",
                "Error"
            )

    def _delete_workout(self):
        """Delete the selected workout after confirmation."""
        workout_id = self._get_selected_workout_id()
        if not workout_id:
            Messagebox.show_warning("Please select a workout to delete.", "No Selection")
            return

        # Get workout info for confirmation
        selected = self.workouts_tree.selection()
        item = self.workouts_tree.item(selected[0])
        values = item['values']
        workout_date = values[0]
        workout_type = values[1]

        # Confirm deletion
        result = Messagebox.okcancel(
            f"Are you sure you want to delete this workout?\n\n"
            f"Date: {workout_date}\n"
            f"Type: {workout_type}\n\n"
            f"This action cannot be undone.",
            "Confirm Deletion"
        )

        if result == "OK":
            try:
                success = delete_workout(workout_id)
                if success:
                    Messagebox.show_info(
                        "Workout deleted successfully.",
                        "Success"
                    )
                    # Reload workouts
                    self._apply_filters()
                else:
                    Messagebox.show_error(
                        "Workout not found or already deleted.",
                        "Delete Error"
                    )
            except Exception as e:
                Messagebox.show_error(
                    f"Error deleting workout:\n{str(e)}",
                    "Delete Error"
                )
