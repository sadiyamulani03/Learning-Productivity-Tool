import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from db_connection import get_connection

class StudySessionModule:

    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.root.title("Study Session Module")
        self.root.geometry("700x500")

        # Subject Dropdown
        tk.Label(root, text="Select Subject").pack()
        self.subject_var = tk.StringVar()
        self.subject_menu = tk.OptionMenu(root, self.subject_var, "")
        self.subject_menu.pack()

        # Start & End Time
        tk.Label(root, text="Start Time (YYYY-MM-DD HH:MM)").pack()
        self.entry_start = tk.Entry(root)
        self.entry_start.pack()
        tk.Label(root, text="End Time (YYYY-MM-DD HH:MM)").pack()
        self.entry_end = tk.Entry(root)
        self.entry_end.pack()

        # Focus & Difficulty
        tk.Label(root, text="Focus Level (1-10)").pack()
        self.entry_focus = tk.Entry(root)
        self.entry_focus.pack()
        tk.Label(root, text="Difficulty Level (1-5)").pack()
        self.entry_difficulty = tk.Entry(root)
        self.entry_difficulty.pack()

        # Notes
        tk.Label(root, text="Notes").pack()
        self.entry_notes = tk.Entry(root, width=50)
        self.entry_notes.pack()

        # Save Button
        tk.Button(root, text="Save Session", command=self.save_session).pack(pady=5)

        # History Listbox
        tk.Label(root, text="Study History").pack()
        self.history_list = tk.Listbox(root, width=100)
        self.history_list.pack(pady=10, fill=tk.BOTH, expand=True)

        # Load subjects and history
        self.load_subjects()
        self.load_history()

    # 🔹 Load Subjects
    def load_subjects(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT subject_id, subject_name FROM subjects WHERE user_id = %s", (self.user_id,))
            subjects = cursor.fetchall()
            conn.close()

            menu = self.subject_menu["menu"]
            menu.delete(0, "end")

            self.subject_dict = {}
            for subject_id, subject_name in subjects:
                self.subject_dict[subject_name] = subject_id
                menu.add_command(label=subject_name,
                                 command=lambda value=subject_name: self.subject_var.set(value))
            if subjects:
                self.subject_var.set(subjects[0][1])  # default first subject
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    # 🔹 Calculate Duration
    def calculate_duration(self, start_time, end_time):
        duration = end_time - start_time
        return duration.total_seconds() / 3600  # hours

    # 🔹 Save Session
    def save_session(self):
        try:
            subject_name = self.subject_var.get()
            if not subject_name:
                messagebox.showerror("Error", "Select a subject")
                return
            subject_id = self.subject_dict[subject_name]

            start_time = datetime.strptime(self.entry_start.get(), "%Y-%m-%d %H:%M")
            end_time = datetime.strptime(self.entry_end.get(), "%Y-%m-%d %H:%M")
            duration = self.calculate_duration(start_time, end_time)

            focus = int(self.entry_focus.get())
            difficulty = int(self.entry_difficulty.get())
            notes = self.entry_notes.get()

            if focus < 1 or focus > 10:
                raise ValueError("Focus must be 1-10")
            if difficulty < 1 or difficulty > 5:
                raise ValueError("Difficulty must be 1-5")

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO study_sessions
                (user_id, subject_id, start_time, end_time, duration, focus_level, difficulty_level, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (self.user_id, subject_id, start_time, end_time, duration, focus, difficulty, notes))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Session Saved Successfully!")
            self.load_history()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # 🔹 Load Study History
    def load_history(self):
        self.history_list.delete(0, tk.END)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT s.session_id, sub.subject_name, s.start_time, s.end_time, s.duration,
                       s.focus_level, s.difficulty_level, s.notes
                FROM study_sessions s
                JOIN subjects sub ON s.subject_id = sub.subject_id
                WHERE s.user_id = %s
                ORDER BY s.start_time DESC
            """, (self.user_id,))
            sessions = cursor.fetchall()
            conn.close()

            for session in sessions:
                self.history_list.insert(tk.END, f"{session[1]} | {session[2]} - {session[3]} | Duration: {session[4]:.2f}h | Focus: {session[5]} | Difficulty: {session[6]} | Notes: {session[7]}")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

# 🔹 Run standalone for testing
if __name__ == "__main__":
    root = tk.Tk()
    user_id = int(input("Enter your user_id to test: "))
    app = StudySessionModule(root, user_id)
    root.mainloop()
