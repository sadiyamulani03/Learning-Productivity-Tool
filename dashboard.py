# dashboard.py
import tkinter as tk
from subject import SubjectModule
from studySessions import StudySessionModule
from analytics import AnalyticsModule
from fatigue import FatigueDetectionModule
from goal import GoalModule
from notification import NotificationModule
from report import ReportModule
from settings import SettingsModule

class Dashboard:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id

        self.root.title("Learning Productivity Dashboard")
        self.root.geometry("550x650")

        tk.Label(root, text="Dashboard", font=("Arial", 16, "bold")).pack(pady=20)

        # Buttons for all modules
        tk.Button(root, text="Manage Subjects", width=30, command=self.openSubjects).pack(pady=5)
        tk.Button(root, text="Add Study Session", width=30, command=self.open_studySession).pack(pady=5)
        tk.Button(root, text="View Analytics", width=30, command=self.open_analytics).pack(pady=5)
        tk.Button(root, text="Check Fatigue", width=30, command=self.open_fatigue).pack(pady=5)
        tk.Button(root, text="Goal Management", width=30, command=self.open_goal).pack(pady=5)
        tk.Button(root, text="Notifications", width=30, command=self.open_notifications).pack(pady=5)
        tk.Button(root, text="Reports & Export", width=30, command=self.open_reports).pack(pady=5)
        tk.Button(root, text="Settings", width=30, command=self.open_settings).pack(pady=5)

    # Module Openers
    def openSubjects(self):
        subject_window = tk.Toplevel(self.root)
        SubjectModule(subject_window, self.user_id)

    def open_studySession(self):
        session_window = tk.Toplevel(self.root)
        StudySessionModule(session_window, self.user_id)

    def open_analytics(self):
        analytics_window = tk.Toplevel(self.root)
        AnalyticsModule(analytics_window, self.user_id)

    def open_fatigue(self):
        fatigue_window = tk.Toplevel(self.root)
        FatigueDetectionModule(fatigue_window, self.user_id)

    def open_goal(self):
        goal_window = tk.Toplevel(self.root)
        GoalModule(goal_window, self.user_id)

    def open_notifications(self):
        notif_window = tk.Toplevel(self.root)
        NotificationModule(notif_window, self.user_id)

    def open_reports(self):
        report_window = tk.Toplevel(self.root)
        ReportModule(report_window, self.user_id)

    def open_settings(self):
        settings_window = tk.Toplevel(self.root)
        SettingsModule(settings_window, self.user_id)


# 🔹 Run standalone for testing
if __name__ == "__main__":
    root = tk.Tk()
    user_id = int(input("Enter user_id to test Dashboard: "))
    Dashboard(root, user_id)
    root.mainloop()
