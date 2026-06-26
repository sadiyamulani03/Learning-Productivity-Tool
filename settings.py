import tkinter as tk
from tkinter import messagebox, filedialog
from db_connection import getConnection
from datetime import datetime
import bcrypt
import csv

class SettingsModule:
    def __init__(self, root, userId):
        self.root = root
        self.userId = userId
        self.root.title("Settings")
        self.root.geometry("450x600")

        tk.Label(root, text="Settings", font=("Arial", 16, "bold")).pack(pady=10)

        # ───── Theme Selection ─────
        tk.Label(root, text="Theme").pack()
        self.themeVar = tk.StringVar(value="Light")
        tk.OptionMenu(root, self.themeVar, "Light", "Dark").pack(pady=5)

        # ───── Reminder Settings ─────
        tk.Label(root, text="Daily Reminder Time (HH:MM)").pack()
        self.entryReminder = tk.Entry(root)
        self.entryReminder.pack(pady=5)

        # ───── Profile Update ─────
        tk.Label(root, text="Full Name").pack()
        self.entryFullname = tk.Entry(root)
        self.entryFullname.pack(pady=5)

        tk.Label(root, text="Email").pack()
        self.entryEmail = tk.Entry(root)
        self.entryEmail.pack(pady=5)

        tk.Label(root, text="Change Password").pack()
        self.entryPassword = tk.Entry(root, show="*")
        self.entryPassword.pack(pady=5)

        # ───── Notification Preferences ─────
        tk.Label(root, text="Notification Preferences").pack(pady=10)
        self.notifyGoal = tk.IntVar()
        self.notifyFatigue = tk.IntVar()
        self.notifyStudy = tk.IntVar()
        tk.Checkbutton(root, text="Goal Alerts", variable=self.notifyGoal).pack()
        tk.Checkbutton(root, text="Fatigue Alerts", variable=self.notifyFatigue).pack()
        tk.Checkbutton(root, text="Study Suggestions", variable=self.notifyStudy).pack()

        # ───── Auto Logout ─────
        tk.Label(root, text="Auto Logout (minutes, 0=disabled)").pack(pady=10)
        self.entryLogout = tk.Entry(root)
        self.entryLogout.pack(pady=5)

        # ───── Buttons ─────
        tk.Button(root, text="Save Settings", command=self.saveSettings).pack(pady=10)
        tk.Button(root, text="Export Study Data", command=self.exportData).pack(pady=5)
        tk.Button(root, text="Reset to Defaults", command=self.resetDefaults).pack(pady=5)

        self.loadSettings()

    # ───── Load current settings ─────
    def loadSettings(self):
        try:
            conn = getConnection()
            cursor = conn.cursor()

            # Settings table
            cursor.execute("SELECT theme, reminderTime, notifyGoal, notifyFatigue, notifyStudy, autoLogout FROM settings WHERE userId=%s", (self.userId,))
            row = cursor.fetchone()
            if row:
                theme, reminderTime, ng, nf, ns, logout = row
                self.themeVar.set(theme)
                if reminderTime:
                    self.entryReminder.insert(0, reminderTime.strftime("%H:%M"))
                self.notifyGoal.set(ng or 0)
                self.notifyFatigue.set(nf or 0)
                self.notifyStudy.set(ns or 0)
                self.entryLogout.insert(0, str(logout or 0))

            # User profile
            cursor.execute("SELECT fullName, email FROM users WHERE userId=%s", (self.userId,))
            userRow = cursor.fetchone()
            if userRow:
                fullName, email = userRow
                self.entryFullname.insert(0, fullName)
                self.entryEmail.insert(0, email)

            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ───── Save Settings ─────
    def saveSettings(self):
        try:
            theme = self.themeVar.get()
            reminder = self.entryReminder.get()
            fullname = self.entryFullname.get()
            email = self.entryEmail.get()
            password = self.entryPassword.get()
            notifyGoal = self.notifyGoal.get()
            notifyFatigue = self.notifyFatigue.get()
            notifyStudy = self.notifyStudy.get()
            autoLogout = int(self.entryLogout.get() or 0)

            if reminder:
                reminderTimeObj = datetime.strptime(reminder, "%H:%M").time()
            else:
                reminderTimeObj = None

            conn = getConnection()
            cursor = conn.cursor()

            # Update settings
            cursor.execute("""
                INSERT INTO settings (user_id, theme, reminder_time, notify_goal, notify_fatigue, notify_study, auto_logout)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
                ON DUPLICATE KEY UPDATE
                    theme=%s, reminder_time=%s, notify_goal=%s, notify_fatigue=%s, notify_study=%s, auto_logout=%s
            """, (self.user_id, theme, reminder_time_obj, notify_goal, notify_fatigue, notify_study, auto_logout,
                  theme, reminder_time_obj, notify_goal, notify_fatigue, notify_study, auto_logout))

            # Update user
            if password:
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                cursor.execute("UPDATE users SET full_name=%s, email=%s, password_hash=%s WHERE user_id=%s",
                               (fullname, email, hashed_password, self.user_id))
            else:
                cursor.execute("UPDATE users SET full_name=%s, email=%s WHERE user_id=%s",
                               (fullname, email, self.user_id))

            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Settings saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ───── Export Study Data ─────
    def export_data(self):
        try:
            conn = getConnection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT s.startTime, s.endTime, sub.subjectName, s.duration, s.focusLevel, s.difficultyLevel, s.notes
                FROM studySessions s
                JOIN subjects sub ON s.subjectId=sub.subjectId
                WHERE s.userId=%s
            """, (self.userId,))
            rows = cursor.fetchall()
            conn.close()

            filePath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")])
            if not filePath:
                return

            with open(filePath, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Start Time", "End Time", "Subject", "Duration", "Focus", "Difficulty", "Notes"])
                writer.writerows(rows)

            messagebox.showinfo("Success", f"Data exported to {filePath}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ───── Reset Settings ─────
    def reset_defaults(self):
        if messagebox.askyesno("Reset", "Are you sure you want to reset all settings to defaults?"):
            try:
                conn = getConnection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM settings WHERE userId=%s", (self.userId,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Reset", "Settings reset to default. Please restart the module.")
                self.root.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
