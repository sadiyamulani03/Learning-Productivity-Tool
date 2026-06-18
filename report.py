import tkinter as tk
from tkinter import messagebox, filedialog
import csv
from datetime import datetime, timedelta
from db_connection import getConnection

class ReportModule:
    def __init__(self, root, userId):
        self.root = root
        self.userId = userId
        self.root.title("Reports & Export")
        self.root.geometry("500x400")

        tk.Label(root, text="Reports & Export", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Button(root, text="Generate Weekly Report", width=30, command=self.weeklyReport).pack(pady=5)
        tk.Button(root, text="Generate Monthly Report", width=30, command=self.monthlyReport).pack(pady=5)
        tk.Button(root, text="Export to CSV", width=30, command=self.exportToCSV).pack(pady=5)

        self.reportText = tk.Text(root, height=15, width=60)
        self.reportText.pack(pady=10)

        self.lastReport = []  # Store last generated report for export

    # Fetch sessions in a period
    def fetchSessions(self, startDate, endDate):
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT sub.subjectName, startTime, endTime, duration, focusLevel, difficultyLevel, notes
            FROM studySessions s
            JOIN subjects sub ON s.subjectId = sub.subjectId
            WHERE s.userId=%s AND s.startTime BETWEEN %s AND %s
            ORDER BY s.startTime
        """, (self.userId, startDate, endDate))
        sessions = cursor.fetchall()
        conn.close()
        return sessions

    # Generate weekly report
    def weeklyReport(self):
        today = datetime.today()
        startDate = today - timedelta(days=today.weekday())  # Monday
        endDate = startDate + timedelta(days=6)             # Sunday
        self.generate_report(startDate, endDate, "Weekly")

    # Generate monthly report
    def monthlyReport(self):
        today = datetime.today()
        startDate = today.replace(day=1)
        nextMonth = startDate.replace(day=28) + timedelta(days=4)
        endDate = nextMonth - timedelta(days=nextMonth.day)
        self.generateReport(startDate, endDate, "Monthly")

    # Core report generation
    def generateReport(self, startDate, endDate, reportType):
        sessions = self.fetchSessions(startDate, endDate)

        if not sessions:
            messagebox.showinfo(reportType + " Report", "No study sessions found for this period.")
            return

        totalHours = sum([float(s[3]) for s in sessions])
        avgFocus = sum([float(s[4]) for s in sessions]) / len(sessions)
        avgDifficulty = sum([float(s[5]) for s in sessions]) / len(sessions)
        productivityScore = (avgFocus * totalHours) / avgDifficulty

        report_lines = [
            f"{reportType} Report ({startDate.date()} to {endDate.date()})\n",
            f"Total Hours: {round(totalHours,2)}",
            f"Average Focus: {round(avgFocus,2)}",
            f"Average Difficulty: {round(avgDifficulty,2)}",
            f"Productivity Score: {round(productivityScore,2)}",
            "\nSessions:\n"
        ]

        for s in sessions:
            subject, start, end, duration, focus, difficulty, notes = s
            reportLines.append(f"{start} - {end} | {subject} | {round(duration,2)} hrs | Focus: {focus} | Difficulty: {difficulty} | Notes: {notes}")

        self.reportText.delete(1.0, tk.END)
        self.reportText.insert(tk.END, "\n".join(reportLines))

        # Store last report for export
        self.lastReport = [["Start Time", "End Time", "Subject", "Duration", "Focus", "Difficulty", "Notes"]] + [
            [s[1], s[2], s[0], s[3], s[4], s[5], s[6]] for s in sessions
        ]

    # Export to CSV
    def exportToCSV(self):
        if not self.lastReport:
            messagebox.showwarning("Export", "No report to export. Generate a report first.")
            return

        filePath = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv")])
        if filePath:
            try:
                with open(filePath, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(self.lastReport)
                messagebox.showinfo("Export", f"Report exported successfully to {filePath}")
            except Exception as e:
                messagebox.showerror("Export Error", str(e))
