import tkinter as tk
from tkinter import messagebox, filedialog
from db_connection import get_connection
from datetime import datetime
import bcrypt
import csv

class SettingsModule:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.root.title("Settings")
        self.root.geometry("450x600")

        tk.Label(root, text="Settings", font=("Arial", 16, "bold")).pack(pady=10)

        # ───── Theme Selection ─────
        tk.Label(root, text="Theme").pack()
        self.theme_var = tk.StringVar(value="Light")
        tk.OptionMenu(root, self.theme_var, "Light", "Dark").pack(pady=5)

        # ───── Reminder Settings ─────
        tk.Label(root, text="Daily Reminder Time (HH:MM)").pack()
        self.entry_reminder = tk.Entry(root)
        self.entry_reminder.pack(pady=5)

        # ───── Profile Update ─────
        tk.Label(root, text="Full Name").pack()
        self.entry_fullname = tk.Entry(root)
        self.entry_fullname.pack(pady=5)

        tk.Label(root, text="Email").pack()
        self.entry_email = tk.Entry(root)
        self.entry_email.pack(pady=5)

        tk.Label(root, text="Change Password").pack()
        self.entry_password = tk.Entry(root, show="*")
        self.entry_password.pack(pady=5)

        # ───── Notification Preferences ─────
        tk.Label(root, text="Notification Preferences").pack(pady=10)
        self.notify_goal = tk.IntVar()
        self.notify_fatigue = tk.IntVar()
        self.notify_study = tk.IntVar()
        tk.Checkbutton(root, text="Goal Alerts", variable=self.notify_goal).pack()
        tk.Checkbutton(root, text="Fatigue Alerts", variable=self.notify_fatigue).pack()
        tk.Checkbutton(root, text="Study Suggestions", variable=self.notify_study).pack()

        # ───── Auto Logout ─────
        tk.Label(root, text="Auto Logout (minutes, 0=disabled)").pack(pady=10)
        self.entry_logout = tk.Entry(root)
        self.entry_logout.pack(pady=5)

        # ───── Buttons ─────
        tk.Button(root, text="Save Settings", command=self.save_settings).pack(pady=10)
        tk.Button(root, text="Export Study Data", command=self.export_data).pack(pady=5)
        tk.Button(root, text="Reset to Defaults", command=self.reset_defaults).pack(pady=5)

        self.load_settings()

    # ───── Load current settings ─────
    def load_settings(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Settings table
            cursor.execute("SELECT theme, reminder_time, notify_goal, notify_fatigue, notify_study, auto_logout FROM settings WHERE user_id=%s", (self.user_id,))
            row = cursor.fetchone()
            if row:
                theme, reminder_time, ng, nf, ns, logout = row
                self.theme_var.set(theme)
                if reminder_time:
                    self.entry_reminder.insert(0, reminder_time.strftime("%H:%M"))
                self.notify_goal.set(ng or 0)
                self.notify_fatigue.set(nf or 0)
                self.notify_study.set(ns or 0)
                self.entry_logout.insert(0, str(logout or 0))

            # User profile
            cursor.execute("SELECT full_name, email FROM users WHERE user_id=%s", (self.user_id,))
            user_row = cursor.fetchone()
            if user_row:
                full_name, email = user_row
                self.entry_fullname.insert(0, full_name)
                self.entry_email.insert(0, email)

            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ───── Save Settings ─────
    def save_settings(self):
        try:
            theme = self.theme_var.get()
            reminder = self.entry_reminder.get()
            fullname = self.entry_fullname.get()
            email = self.entry_email.get()
            password = self.entry_password.get()
            notify_goal = self.notify_goal.get()
            notify_fatigue = self.notify_fatigue.get()
            notify_study = self.notify_study.get()
            auto_logout = int(self.entry_logout.get() or 0)

            if reminder:
                reminder_time_obj = datetime.strptime(reminder, "%H:%M").time()
            else:
                reminder_time_obj = None

            conn = get_connection()
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
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT s.start_time, s.end_time, sub.subject_name, s.duration, s.focus_level, s.difficulty_level, s.notes
                FROM study_sessions s
                JOIN subjects sub ON s.subject_id=sub.subject_id
                WHERE s.user_id=%s
            """, (self.user_id,))
            rows = cursor.fetchall()
            conn.close()

            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")])
            if not file_path:
                return

            with open(file_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Start Time", "End Time", "Subject", "Duration", "Focus", "Difficulty", "Notes"])
                writer.writerows(rows)

            messagebox.showinfo("Success", f"Data exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ───── Reset Settings ─────
    def reset_defaults(self):
        if messagebox.askyesno("Reset", "Are you sure you want to reset all settings to defaults?"):
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM settings WHERE user_id=%s", (self.user_id,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Reset", "Settings reset to default. Please restart the module.")
                self.root.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
