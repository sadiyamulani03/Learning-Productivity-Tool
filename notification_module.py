import tkinter as tk
from tkinter import messagebox
from db_connection import get_connection
from datetime import datetime, timedelta

class NotificationModule:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.root.title("Notifications")
        self.root.geometry("400x300")

        tk.Label(root, text="Notifications", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Button(root, text="Check Notifications", command=self.show_notifications).pack(pady=10)

        self.listbox = tk.Listbox(root, width=50)
        self.listbox.pack(pady=10, fill=tk.BOTH, expand=True)

    # Fetch notifications from DB
    def show_notifications(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT notification_id, message, status, created_at
                FROM notifications
                WHERE user_id=%s
                ORDER BY created_at DESC
            """, (self.user_id,))
            notifications = cursor.fetchall()
            conn.close()

            self.listbox.delete(0, tk.END)

            if not notifications:
                self.listbox.insert(tk.END, "No notifications found.")
                return

            for notif_id, message, status, created_at in notifications:
                self.listbox.insert(tk.END, f"[{status}] {created_at.strftime('%Y-%m-%d %H:%M')} - {message}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Optional: add a notification
    @staticmethod
    def add_notification(user_id, message):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO notifications (user_id, message, status)
            VALUES (%s, %s, 'Unread')
        """, (user_id, message))
        conn.commit()
        conn.close()
