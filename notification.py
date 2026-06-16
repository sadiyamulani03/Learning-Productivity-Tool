import tkinter as tk
from tkinter import messagebox
from db_connection import getConnection
from datetime import datetime, timedelta

class NotificationModule:
    def __init__(self, root, user_id):
        self.root = root
        self.userId = userId
        self.root.title("Notifications")
        self.root.geometry("400x300")

        tk.Label(root, text="Notifications", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Button(root, text="Check Notifications", command=self.showNotifications).pack(pady=10)

        self.listbox = tk.Listbox(root, width=50)
        self.listbox.pack(pady=10, fill=tk.BOTH, expand=True)

    # Fetch notifications from DB
    def showNotifications(self):
        try:
            conn = getConnection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT notificationId, message, status, createdAt
                FROM notifications
                WHERE userId=%s
                ORDER BY createdAt DESC
            """, (self.userId,))
            notifications = cursor.fetchall()
            conn.close()

            self.listbox.delete(0, tk.END)

            if not notifications:
                self.listbox.insert(tk.END, "No notifications found.")
                return

            for notifId, message, status, createdAt in notifications:
                self.listbox.insert(tk.END, f"[{status}] {createdAt.strftime('%Y-%m-%d %H:%M')} - {message}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Optional: add a notification
    @staticmethod
    def addNotification(userId, message):
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO notifications (userId, message, status)
            VALUES (%s, %s, 'Unread')
        """, (userId, message))
        conn.commit()
        conn.close()
