import tkinter as tk
from tkinter import messagebox
from db_connection import get_connection
from datetime import date, datetime, timedelta

class GoalModule:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.root.title("Goal Management")
        self.root.geometry("450x400")

        tk.Label(root, text="Goal Management", font=("Arial", 14, "bold")).pack(pady=10)

        # Set Goal
        tk.Label(root, text="Target Hours").pack()
        self.entry_target = tk.Entry(root)
        self.entry_target.pack(pady=5)

        tk.Label(root, text="Start Date (YYYY-MM-DD)").pack()
        self.entry_start = tk.Entry(root)
        self.entry_start.pack(pady=5)

        tk.Label(root, text="End Date (YYYY-MM-DD)").pack()
        self.entry_end = tk.Entry(root)
        self.entry_end.pack(pady=5)

        tk.Button(root, text="Set Goal", command=self.set_goal).pack(pady=10)
        tk.Button(root, text="View Progress", command=self.view_progress).pack(pady=5)

        self.progress_label = tk.Label(root, text="", font=("Arial", 12), fg="green")
        self.progress_label.pack(pady=10)

    # Set a new goal
    def set_goal(self):
        try:
            target_hours = float(self.entry_target.get())
            start_date = datetime.strptime(self.entry_start.get(), "%Y-%m-%d").date()
            end_date = datetime.strptime(self.entry_end.get(), "%Y-%m-%d").date()

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO goals (user_id, target_hours, start_date, end_date)
                VALUES (%s, %s, %s, %s)
            """, (self.user_id, target_hours, start_date, end_date))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Goal Set Successfully!")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # View progress and completion %
    def view_progress(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Get active goal
            cursor.execute("""
                SELECT goal_id, target_hours, start_date, end_date
                FROM goals
                WHERE user_id = %s AND status='Active'
                ORDER BY created_at DESC
                LIMIT 1
            """, (self.user_id,))
            goal = cursor.fetchone()

            if not goal:
                messagebox.showinfo("Info", "No active goal found")
                return

            goal_id, target_hours, start_date, end_date = goal

            # Sum study hours in goal period
            cursor.execute("""
                SELECT SUM(duration)
                FROM study_sessions
                WHERE user_id = %s AND start_time BETWEEN %s AND %s
            """, (self.user_id, start_date, end_date))
            studied_hours = cursor.fetchone()[0] or 0
            studied_hours = float(studied_hours)

            completion_percent = (studied_hours / float(target_hours)) * 100

            # Update goal status if completed
            if completion_percent >= 100:
                cursor.execute("UPDATE goals SET status='Completed' WHERE goal_id=%s", (goal_id,))
                conn.commit()

            conn.close()

            self.progress_label.config(
                text=f"Progress: {round(completion_percent,2)}% ({studied_hours}/{target_hours} hours)"
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))
