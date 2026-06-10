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
    def __init__(self, root, userId):
        self.root = root
        self.userId = userId

        self.root.title("Learning Productivity Dashboard")
        self.root.geometry("550x650")

        tk.Label(root, text="Dashboard", font=("Arial", 16, "bold")).pack(pady=20)

        # Buttons for all modules
        tk.Button(root, text="Manage Subjects", width=30, command=self.openSubjects).pack(pady=5)
        tk.Button(root, text="Add Study Session", width=30, command=self.openStudySession).pack(pady=5)
        tk.Button(root, text="View Analytics", width=30, command=self.openAnalytics).pack(pady=5)
        tk.Button(root, text="Check Fatigue", width=30, command=self.openFatigue).pack(pady=5)
        tk.Button(root, text="Goal Management", width=30, command=self.openGoal).pack(pady=5)
        tk.Button(root, text="Notifications", width=30, command=self.openNotifications).pack(pady=5)
        tk.Button(root, text="Reports & Export", width=30, command=self.openReports).pack(pady=5)
        tk.Button(root, text="Settings", width=30, command=self.openSettings).pack(pady=5)

    # Module Openers
    def openSubjects(self):
        subjectWindow = tk.Toplevel(self.root)
        SubjectModule(subjectWindow, self.userId)

    def openStudySession(self):
        sessionWindow = tk.Toplevel(self.root)
        StudySessionModule(sessionWindow, self.userId)

    def openAnalytics(self):
        analyticsWindow = tk.Toplevel(self.root)
        AnalyticsModule(analyticsWindow, self.userId)

    def openFatigue(self):
        fatigueWindow = tk.Toplevel(self.root)
        FatigueDetectionModule(fatigueWindow, self.userId)

    def openGoal(self):
        goalWindow = tk.Toplevel(self.root)
        GoalModule(goalWindow, self.userId)

    def openNotifications(self):
        notifWindow = tk.Toplevel(self.root)
        NotificationModule(notifWindow, self.userId)

    def openReports(self):
        reportWindow = tk.Toplevel(self.root)
        ReportModule(reportWindow, self.userId)

    def openSettings(self):
        settingsWindow = tk.Toplevel(self.root)
        SettingsModule(settingsWindow, self.userId)


# 🔹 Run standalone for testing
if __name__ == "__main__":
    root = tk.Tk()
    userId = int(input("Enter user_id to test Dashboard: "))
    Dashboard(root, userId)
    root.mainloop()
