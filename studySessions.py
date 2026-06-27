import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from db_connection import getConnection

class StudySessionModule:

    def __init__(self, root, userId):
        self.root = root
        self.userId = userId
        self.root.title("Study Session Module")
        self.root.geometry("700x500")

        # Subject Dropdown
        tk.Label(root, text="Select Subject").pack()
        self.subjectVar = tk.StringVar()
        self.subjectMenu = tk.OptionMenu(root, self.subjectVar, "")
        self.subjectMenu.pack()

        # Start & End Time
        tk.Label(root, text="Start Time (YYYY-MM-DD HH:MM)").pack()
        self.entryStart = tk.Entry(root)
        self.entryStart.pack()
        tk.Label(root, text="End Time (YYYY-MM-DD HH:MM)").pack()
        self.entryEnd = tk.Entry(root)
        self.entryEnd.pack()

        # Focus & Difficulty
        tk.Label(root, text="Focus Level (1-10)").pack()
        self.entryFocus = tk.Entry(root)
        self.entryFocus.pack()
        tk.Label(root, text="Difficulty Level (1-5)").pack()
        self.entryDifficulty = tk.Entry(root)
        self.entryDifficulty.pack()

        # Notes
        tk.Label(root, text="Notes").pack()
        self.entryNotes = tk.Entry(root, width=50)
        self.entryNotes.pack()

        # Save Button
        tk.Button(root, text="Save Session", command=self.saveSession).pack(pady=5)

        # History Listbox
        tk.Label(root, text="Study History").pack()
        self.historyList = tk.Listbox(root, width=100)
        self.historyList.pack(pady=10, fill=tk.BOTH, expand=True)

        # Load subjects and history
        self.loadSubjects()
        self.loadHistory()

    # 🔹 Load Subjects
    def loadSubjects(self):
        try:
            conn = getConnection()
            cursor = conn.cursor()
            cursor.execute("SELECT subjectId, subjectName FROM subjects WHERE userId = %s", (self.userId,))
            subjects = cursor.fetchall()
            conn.close()

            menu = self.subjectMenu["menu"]
            menu.delete(0, "end")

            self.subjectDict = {}
            for subjectId, subjectName in subjects:
                self.subjectDict[subject_name] = subjectId
                menu.addCommand(label=subjectName,
                                 command=lambda value=subjectName: self.subjectVar.set(value))
            if subjects:
                self.subjectVar.set(subjects[0][1])  # default first subject
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    # 🔹 Calculate Duration
    def calculateDuration(self, startTime, endTime):
        duration = endTime - startTime
        return duration.totalSeconds() / 3600  # hours

    # 🔹 Save Session
    def saveSession(self):
        try:
            subjectName = self.subjectVar.get()
            if not subjectName:
                messagebox.showerror("Error", "Select a subject")
                return
            subjectId = self.subjectDict[subjectName]

            startTime = datetime.strptime(self.entryStart.get(), "%Y-%m-%d %H:%M")
            endTime = datetime.strptime(self.entryEnd.get(), "%Y-%m-%d %H:%M")
            duration = self.calculateDuration(startTime, endTime)

            focus = int(self.entryFocus.get())
            difficulty = int(self.entryDifficulty.get())
            notes = self.entryNotes.get()

            if focus < 1 or focus > 10:
                raise ValueError("Focus must be 1-10")
            if difficulty < 1 or difficulty > 5:
                raise ValueError("Difficulty must be 1-5")

            conn = getConnection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO study_sessions
                (userId, subjectId, startTime, endTime, duration, focusLevel, difficultyLevel, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (self.userId, subjectId, startTime, endTime, duration, focus, difficulty, notes))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Session Saved Successfully!")
            self.loadHistory()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # 🔹 Load Study History
    def loadHistory(self):
        self.historyList.delete(0, tk.END)
        try:
            conn = getConnection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT s.sessionId, sub.subjectName, s.startTime, s.endTime, s.duration,
                       s.focusLevel, s.difficultyLevel, s.notes
                FROM studySessions s
                JOIN subjects sub ON s.subjectId = sub.subjectId
                WHERE s.userId = %s
                ORDER BY s.startTime DESC
            """, (self.userId,))
            sessions = cursor.fetchall()
            conn.close()

            for session in sessions:
                self.historyList.insert(tk.END, f"{session[1]} | {session[2]} - {session[3]} | Duration: {session[4]:.2f}h | Focus: {session[5]} | Difficulty: {session[6]} | Notes: {session[7]}")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

# 🔹 Run standalone for testing
if __name__ == "__main__":
    root = tk.Tk()
    userId = int(input("Enter your userId to test: "))
    app = StudySessionModule(root, userId)
    root.mainloop()
