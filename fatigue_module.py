import tkinter as tk
from tkinter import messagebox
from db_connection import get_connection
from datetime import datetime, timedelta

class FatigueDetectionModule:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.root.title("Fatigue Detection")
        self.root.geometry("400x300")

        tk.Label(root, text="Fatigue Detection Module", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Button(root, text="Analyze Fatigue", command=self.analyze_fatigue).pack(pady=10)
        
        self.result_label = tk.Label(root, text="", font=("Arial", 12), fg="red")
        self.result_label.pack(pady=10)
        
        self.recommendation_label = tk.Label(root, text="", font=("Arial", 10), fg="blue")
        self.recommendation_label.pack(pady=10)

    # 🔹 Core Fatigue Logic
    def analyze_fatigue(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        # Fetch last 7 study sessions for the user
        cursor.execute("""
            SELECT start_time, duration, focus_level
            FROM study_sessions
            WHERE user_id = %s
            ORDER BY start_time DESC
            LIMIT 7
        """, (self.user_id,))
        
        sessions = cursor.fetchall()
        conn.close()
        
        if not sessions:
            messagebox.showinfo("Info", "No study sessions found.")
            return
        
        # Calculate trends
        focus_values = [row[2] for row in sessions]
        duration_values = [row[1] for row in sessions]
        
        # Simple trend: last - first
        focus_trend = focus_values[-1] - focus_values[0]  # negative => decreasing focus
        duration_trend = duration_values[-1] - duration_values[0]  # positive => increasing duration
        
        # Fatigue logic thresholds (customize as needed)
        focus_threshold = -2  # focus decreased by 2 or more
        duration_threshold = 2  # duration increased by 2 hours or more
        
        fatigue_score = abs(focus_trend) * duration_trend  # simple score calculation
        fatigue_alert = False
        
        if focus_trend < focus_threshold and duration_trend > duration_threshold:
            fatigue_alert = True
            message = f"⚠️ Fatigue Detected! Score: {round(fatigue_score,2)}"
            recommendation = "💡 Take a short break, relax, and avoid long continuous sessions."
        else:
            message = f"✅ Fatigue level normal. Score: {round(fatigue_score,2)}"
            recommendation = "Keep up the good study habits!"
        
        # Display results
        self.result_label.config(text=message)
        self.recommendation_label.config(text=recommendation)
