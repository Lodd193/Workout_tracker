# workout_tracker/ui/log_workout_view.py

from datetime import datetime
from tkinter import ttk, messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from ..services.workout_service import save_workout, get_exercises


class LogWorkoutView(tb.Frame):
    """Tab for logging workouts with exercises, sets, and cardio."""

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.sets_data = []  # Store sets temporarily before saving
        self._build_ui()

    def _build_ui(self):
        """Build the complete Log Workout interface."""

        # Main container with padding
        container = tb.Frame(self, padding=20)
        container.pack(fill=BOTH, expand=YES)

        # Title
        title = tb.Label(
            container,
            text="Log Workout",
            font=("Helvetica", 18, "bold"),
            bootstyle="inverse-primary"
        )
        title.pack(pady=(0, 20))

        # ===== WORKOUT INFO SECTION =====
        info_frame = tb.Labelframe(container, text="Workout Information", padding=15)
        info_frame.pack(fill=X, pady=(0, 15))

        # Date picker
        date_row = tb.Frame(info_frame)
        date_row.pack(fill=X, pady=5)
        tb.Label(date_row, text="Date:", width=15).pack(side=LEFT)
        self.date_entry = tb.DateEntry(date_row, dateformat="%Y-%m-%d")
        self.date_entry.pack(side=LEFT, fill=X, expand=YES)

        # Workout type dropdown (optional)
        type_row = tb.Frame(info_frame)
        type_row.pack(fill=X, pady=5)
        tb.Label(type_row, text="Workout Type (optional):", width=20).pack(side=LEFT)
        self.workout_type_var = tb.StringVar(value="General")
        self.workout_type_combo = tb.Combobox(
            type_row,
            textvariable=self.workout_type_var,
            values=["General", "Push", "Pull", "Legs", "Full Body", "Upper", "Lower", "Cardio"],
            state="readonly"
        )
        self.workout_type_combo.pack(side=LEFT, fill=X, expand=YES)
        self.workout_type_combo.current(0)  # Default to "General"

        # ===== EXERCISE SECTION =====
        exercise_frame = tb.Labelframe(container, text="Exercises & Sets", padding=15)
        exercise_frame.pack(fill=BOTH, expand=YES, pady=(0, 15))

        # Input fields for adding sets
        input_frame = tb.Frame(exercise_frame)
        input_frame.pack(fill=X, pady=(0, 10))

        # Exercise name - Combobox with existing exercises
        tb.Label(input_frame, text="Exercise:", width=10).grid(row=0, column=0, padx=5, sticky=W)
        self.exercise_var = tb.StringVar()
        self.exercise_entry = tb.Combobox(input_frame, textvariable=self.exercise_var, width=20)
        self.exercise_entry.grid(row=0, column=1, padx=5, sticky=EW)
        self._load_exercises()  # Load existing exercises into dropdown

        # Reps
        tb.Label(input_frame, text="Reps:", width=8).grid(row=0, column=2, padx=5, sticky=W)
        self.reps_entry = tb.Entry(input_frame, width=8)
        self.reps_entry.grid(row=0, column=3, padx=5)

        # Weight
        tb.Label(input_frame, text="Weight (lbs):", width=12).grid(row=0, column=4, padx=5, sticky=W)
        self.weight_entry = tb.Entry(input_frame, width=8)
        self.weight_entry.grid(row=0, column=5, padx=5)

        # RPE (optional)
        tb.Label(input_frame, text="RPE:", width=6).grid(row=0, column=6, padx=5, sticky=W)
        self.rpe_entry = tb.Entry(input_frame, width=6)
        self.rpe_entry.grid(row=0, column=7, padx=5)

        # Add Set button
        add_btn = tb.Button(
            input_frame,
            text="Add Set",
            bootstyle="success",
            command=self._add_set
        )
        add_btn.grid(row=0, column=8, padx=10)

        # Configure grid weights
        input_frame.columnconfigure(1, weight=1)

        # Treeview to display sets
        tree_frame = tb.Frame(exercise_frame)
        tree_frame.pack(fill=BOTH, expand=YES)

        # Scrollbar
        scrollbar = tb.Scrollbar(tree_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.sets_tree = ttk.Treeview(
            tree_frame,
            columns=("exercise", "set", "reps", "weight", "rpe"),
            show="headings",
            height=8,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.sets_tree.yview)

        # Define columns
        self.sets_tree.heading("exercise", text="Exercise")
        self.sets_tree.heading("set", text="Set #")
        self.sets_tree.heading("reps", text="Reps")
        self.sets_tree.heading("weight", text="Weight (lbs)")
        self.sets_tree.heading("rpe", text="RPE")

        self.sets_tree.column("exercise", width=200)
        self.sets_tree.column("set", width=60, anchor=CENTER)
        self.sets_tree.column("reps", width=80, anchor=CENTER)
        self.sets_tree.column("weight", width=100, anchor=CENTER)
        self.sets_tree.column("rpe", width=60, anchor=CENTER)

        self.sets_tree.pack(fill=BOTH, expand=YES)

        # Remove Set button
        remove_btn = tb.Button(
            exercise_frame,
            text="Remove Selected Set",
            bootstyle="danger",
            command=self._remove_set
        )
        remove_btn.pack(pady=(10, 0))

        # ===== CARDIO SECTION =====
        cardio_frame = tb.Labelframe(container, text="Cardio (Optional)", padding=15)
        cardio_frame.pack(fill=X, pady=(0, 15))

        cardio_row = tb.Frame(cardio_frame)
        cardio_row.pack(fill=X)

        # Cardio type
        tb.Label(cardio_row, text="Type:", width=15).pack(side=LEFT)
        self.cardio_type_var = tb.StringVar()
        self.cardio_type_combo = tb.Combobox(
            cardio_row,
            textvariable=self.cardio_type_var,
            values=["Walking", "Running", "Cycling", "Rowing", "Swimming", "Elliptical", "Other"],
            width=15
        )
        self.cardio_type_combo.pack(side=LEFT, padx=(0, 20))

        # Cardio minutes
        tb.Label(cardio_row, text="Minutes:", width=10).pack(side=LEFT)
        self.cardio_minutes_entry = tb.Entry(cardio_row, width=10)
        self.cardio_minutes_entry.pack(side=LEFT)

        # ===== NOTES SECTION =====
        notes_frame = tb.Labelframe(container, text="Notes (Optional)", padding=15)
        notes_frame.pack(fill=X, pady=(0, 15))

        self.notes_text = tb.Text(notes_frame, height=4, width=50)
        self.notes_text.pack(fill=BOTH, expand=YES)

        # ===== ACTION BUTTONS =====
        button_frame = tb.Frame(container)
        button_frame.pack(fill=X, pady=(10, 0))

        save_btn = tb.Button(
            button_frame,
            text="Save Workout",
            bootstyle="primary",
            command=self._save_workout,
            width=20
        )
        save_btn.pack(side=LEFT, padx=(0, 10))

        clear_btn = tb.Button(
            button_frame,
            text="Clear All",
            bootstyle="secondary",
            command=self._clear_form,
            width=20
        )
        clear_btn.pack(side=LEFT)

    def _load_exercises(self):
        """Load existing exercises from database and predefined exercises into the dropdown."""
        # Predefined common exercises
        predefined_exercises = [
            "Barbell Bench Press",
            "Barbell Squat",
            "Deadlift",
            "Barbell Row",
            "Overhead Press",
            "Cable Chest Fly",
            "Cable Delt Raise",
            "Face Pulls",
            "Hamstring Curl Machine",
            "Quad Extension Machine",
            "Leg Press",
            "Calves Press",
            "Pull-ups",
            "Dips",
            "Lateral Raises",
            "Bicep Curls",
            "Tricep Extensions",
            "Romanian Deadlift"
        ]

        try:
            # Get exercises from database
            db_exercises = get_exercises()

            # Combine and remove duplicates (case-insensitive)
            all_exercises = predefined_exercises.copy()
            if db_exercises:
                for ex in db_exercises:
                    if ex not in all_exercises:
                        all_exercises.append(ex)

            # Sort alphabetically for easier finding
            all_exercises.sort()

            self.exercise_entry['values'] = all_exercises

        except Exception as e:
            # If there's an error loading from database, use predefined list
            self.exercise_entry['values'] = sorted(predefined_exercises)

    def _add_set(self):
        """Add a set to the workout."""
        exercise = self.exercise_entry.get().strip()
        reps = self.reps_entry.get().strip()
        weight = self.weight_entry.get().strip()
        rpe = self.rpe_entry.get().strip()

        # Validation
        if not exercise:
            Messagebox.show_error("Please enter an exercise name.", "Validation Error")
            return

        if not reps or not reps.isdigit():
            Messagebox.show_error("Please enter a valid number of reps.", "Validation Error")
            return

        try:
            weight_val = float(weight)
        except ValueError:
            Messagebox.show_error("Please enter a valid weight.", "Validation Error")
            return

        # RPE is optional
        rpe_val = None
        if rpe:
            try:
                rpe_val = float(rpe)
                if rpe_val < 0 or rpe_val > 10:
                    Messagebox.show_error("RPE must be between 0 and 10.", "Validation Error")
                    return
            except ValueError:
                Messagebox.show_error("Please enter a valid RPE (0-10).", "Validation Error")
                return

        # Calculate set number for this exercise
        set_number = sum(1 for s in self.sets_data if s['exercise_name'] == exercise) + 1

        # Add to internal data
        set_data = {
            'exercise_name': exercise,
            'set_number': set_number,
            'reps': int(reps),
            'weight': weight_val,
            'rpe': rpe_val
        }
        self.sets_data.append(set_data)

        # Add to treeview
        self.sets_tree.insert(
            "",
            END,
            values=(exercise, set_number, reps, weight_val, rpe_val if rpe_val else "-")
        )

        # Clear input fields for next set (keep exercise name)
        self.reps_entry.delete(0, END)
        self.weight_entry.delete(0, END)
        self.rpe_entry.delete(0, END)
        self.reps_entry.focus()

    def _remove_set(self):
        """Remove the selected set from the workout."""
        selected = self.sets_tree.selection()
        if not selected:
            Messagebox.show_warning("Please select a set to remove.", "No Selection")
            return

        # Get index of selected item
        item_index = self.sets_tree.index(selected[0])

        # Remove from data
        if 0 <= item_index < len(self.sets_data):
            removed_set = self.sets_data.pop(item_index)

            # Renumber remaining sets for the same exercise
            exercise_name = removed_set['exercise_name']
            for i, s in enumerate(self.sets_data):
                if s['exercise_name'] == exercise_name:
                    s['set_number'] = sum(1 for x in self.sets_data[:i+1] if x['exercise_name'] == exercise_name)

        # Remove from treeview
        self.sets_tree.delete(selected[0])

        # Rebuild treeview to reflect renumbering
        self._refresh_tree()

    def _refresh_tree(self):
        """Refresh the treeview to show current sets_data."""
        # Clear treeview
        for item in self.sets_tree.get_children():
            self.sets_tree.delete(item)

        # Repopulate
        for set_data in self.sets_data:
            self.sets_tree.insert(
                "",
                END,
                values=(
                    set_data['exercise_name'],
                    set_data['set_number'],
                    set_data['reps'],
                    set_data['weight'],
                    set_data['rpe'] if set_data['rpe'] else "-"
                )
            )

    def _save_workout(self):
        """Save the workout to the database."""
        # Validate
        if not self.sets_data:
            Messagebox.show_warning(
                "Please add at least one set before saving.",
                "No Sets Added"
            )
            return

        # Get workout type (defaults to "General")
        workout_type = self.workout_type_var.get() or "General"

        # Get date
        date_str = self.date_entry.entry.get()

        # Get cardio data
        cardio_minutes = None
        cardio_type = None
        cardio_input = self.cardio_minutes_entry.get().strip()
        if cardio_input:
            try:
                cardio_minutes = int(cardio_input)
                cardio_type = self.cardio_type_var.get() or "General"
            except ValueError:
                Messagebox.show_error("Please enter a valid number for cardio minutes.", "Validation Error")
                return

        # Get notes
        notes = self.notes_text.get("1.0", END).strip()
        if not notes:
            notes = None

        # Save to database
        try:
            workout_id = save_workout(
                date=date_str,
                workout_type=workout_type,
                sets_data=self.sets_data,
                cardio_minutes=cardio_minutes,
                cardio_type=cardio_type,
                notes=notes
            )

            Messagebox.show_info(
                f"Workout saved successfully!\nWorkout ID: {workout_id}",
                "Success"
            )

            # Reload exercises to include any newly added ones
            self._load_exercises()

            # Clear form
            self._clear_form()

        except Exception as e:
            Messagebox.show_error(
                f"Error saving workout:\n{str(e)}",
                "Save Error"
            )

    def _clear_form(self):
        """Clear all input fields and reset the form."""
        # Clear sets
        self.sets_data = []
        for item in self.sets_tree.get_children():
            self.sets_tree.delete(item)

        # Clear input fields
        self.exercise_entry.delete(0, END)
        self.reps_entry.delete(0, END)
        self.weight_entry.delete(0, END)
        self.rpe_entry.delete(0, END)

        # Reset date to today
        self.date_entry.entry.delete(0, END)
        self.date_entry.entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Reset workout type
        self.workout_type_combo.current(0)

        # Clear cardio
        self.cardio_type_var.set("")
        self.cardio_minutes_entry.delete(0, END)

        # Clear notes
        self.notes_text.delete("1.0", END)
