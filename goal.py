import tkinter as tk
from tkinter import messagebox
from db_connection import getConnection
from datetime import date, datetime, timedelta

class GoalModule:
    def __init__(self, root, userId):
        self.root = root
        self.userId = userId
        self.root.title("Goal Management")
        self.root.geometry("450x400")

        tk.Label(root, text="Goal Management", font=("Arial", 14, "bold")).pack(pady=10)

        # Set Goal
        tk.Label(root, text="Target Hours").pack()
        self.entryTarget = tk.Entry(root)
        self.entryTarget.pack(pady=5)

        tk.Label(root, text="Start Date (YYYY-MM-DD)").pack()
        self.entryStart = tk.Entry(root)
        self.entryStart.pack(pady=5)

        tk.Label(root, text="End Date (YYYY-MM-DD)").pack()
        self.entryEnd = tk.Entry(root)
        self.entryEnd.pack(pady=5)

        tk.Button(root, text="Set Goal", command=self.setGoal).pack(pady=10)
        tk.Button(root, text="View Progress", command=self.viewProgress).pack(pady=5)

        self.progressLabel = tk.Label(root, text="", font=("Arial", 12), fg="green")
        self.progressLabel.pack(pady=10)

    # Set a new goal
    def setGoal(self):
        try:
            targetHours = float(self.entryTarget.get())
            startDate = datetime.strptime(self.entryStart.get(), "%Y-%m-%d").date()
            endDate = datetime.strptime(self.entryEnd.get(), "%Y-%m-%d").date()

            conn = getConnection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO goals (userId, targetHours, startDate, endDate)
                VALUES (%s, %s, %s, %s)
            """, (self.userId, targetHours, startDate, endDate))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Goal Set Successfully!")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # View progress and completion %
    def viewProgress(self):
        try:
            conn = getConnection()
            cursor = conn.cursor()

            # Get active goal
            cursor.execute("""
                SELECT goalId, targetHours, startDate, endDate
                FROM goals
                WHERE userId = %s AND status='Active'
                ORDER BY created_at DESC
                LIMIT 1
            """, (self.userId,))
            goal = cursor.fetchone()

            if not goal:
                messagebox.showinfo("Info", "No active goal found")
                return

            goalId, targetHours, startDate, endDate = goal

            # Sum study hours in goal period
            cursor.execute("""
                SELECT SUM(duration)
                FROM studySessions
                WHERE userId = %s AND startTime BETWEEN %s AND %s
            """, (self.userId, startDate, endDate))
            studiedHours = cursor.fetchone()[0] or 0
            studiedHours = float(studiedHours)

            completionPercent = (studiedHours / float(targetHours)) * 100

            # Update goal status if completed
            if completionPercent >= 100:
                cursor.execute("UPDATE goals SET status='Completed' WHERE goal_id=%s", (goal_id,))
                conn.commit()

            conn.close()

            self.progressLabel.config(
                text=f"Progress: {round(completionPercent,2)}% ({studiedHours}/{targetHours} hours)"
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))
