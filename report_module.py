import tkinter as tk
from tkinter import messagebox, filedialog
import csv
from datetime import datetime, timedelta
from db_connection import get_connection

class ReportModule:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.root.title("Reports & Export")
        self.root.geometry("500x400")

        tk.Label(root, text="Reports & Export", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Button(root, text="Generate Weekly Report", width=30, command=self.weekly_report).pack(pady=5)
        tk.Button(root, text="Generate Monthly Report", width=30, command=self.monthly_report).pack(pady=5)
        tk.Button(root, text="Export to CSV", width=30, command=self.export_to_csv).pack(pady=5)

        self.report_text = tk.Text(root, height=15, width=60)
        self.report_text.pack(pady=10)

        self.last_report = []  # Store last generated report for export

    # Fetch sessions in a period
    def fetch_sessions(self, start_date, end_date):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT sub.subject_name, start_time, end_time, duration, focus_level, difficulty_level, notes
            FROM study_sessions s
            JOIN subjects sub ON s.subject_id = sub.subject_id
            WHERE s.user_id=%s AND s.start_time BETWEEN %s AND %s
            ORDER BY s.start_time
        """, (self.user_id, start_date, end_date))
        sessions = cursor.fetchall()
        conn.close()
        return sessions

    # Generate weekly report
    def weekly_report(self):
        today = datetime.today()
        start_date = today - timedelta(days=today.weekday())  # Monday
        end_date = start_date + timedelta(days=6)             # Sunday
        self.generate_report(start_date, end_date, "Weekly")

    # Generate monthly report
    def monthly_report(self):
        today = datetime.today()
        start_date = today.replace(day=1)
        next_month = start_date.replace(day=28) + timedelta(days=4)
        end_date = next_month - timedelta(days=next_month.day)
        self.generate_report(start_date, end_date, "Monthly")

    # Core report generation
    def generate_report(self, start_date, end_date, report_type):
        sessions = self.fetch_sessions(start_date, end_date)

        if not sessions:
            messagebox.showinfo(report_type + " Report", "No study sessions found for this period.")
            return

        total_hours = sum([float(s[3]) for s in sessions])
        avg_focus = sum([float(s[4]) for s in sessions]) / len(sessions)
        avg_difficulty = sum([float(s[5]) for s in sessions]) / len(sessions)
        productivity_score = (avg_focus * total_hours) / avg_difficulty

        report_lines = [
            f"{report_type} Report ({start_date.date()} to {end_date.date()})\n",
            f"Total Hours: {round(total_hours,2)}",
            f"Average Focus: {round(avg_focus,2)}",
            f"Average Difficulty: {round(avg_difficulty,2)}",
            f"Productivity Score: {round(productivity_score,2)}",
            "\nSessions:\n"
        ]

        for s in sessions:
            subject, start, end, duration, focus, difficulty, notes = s
            report_lines.append(f"{start} - {end} | {subject} | {round(duration,2)} hrs | Focus: {focus} | Difficulty: {difficulty} | Notes: {notes}")

        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(tk.END, "\n".join(report_lines))

        # Store last report for export
        self.last_report = [["Start Time", "End Time", "Subject", "Duration", "Focus", "Difficulty", "Notes"]] + [
            [s[1], s[2], s[0], s[3], s[4], s[5], s[6]] for s in sessions
        ]

    # Export to CSV
    def export_to_csv(self):
        if not self.last_report:
            messagebox.showwarning("Export", "No report to export. Generate a report first.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                with open(file_path, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(self.last_report)
                messagebox.showinfo("Export", f"Report exported successfully to {file_path}")
            except Exception as e:
                messagebox.showerror("Export Error", str(e))
