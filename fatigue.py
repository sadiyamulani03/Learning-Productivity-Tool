import tkinter as tk
from tkinter import messagebox
from db_connection import get_connection
from datetime import datetime, timedelta

class FatigueDetectionModule:
    def __init__(self, root, userId):
        self.root = root
        self.userId = userId
        self.root.title("Fatigue Detection")
        self.root.geometry("400x300")

        tk.Label(root, text="Fatigue Detection Module", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Button(root, text="Analyze Fatigue", command=self.analyzeFatigue).pack(pady=10)
        
        self.resultLabel = tk.Label(root, text="", font=("Arial", 12), fg="red")
        self.resultLabel.pack(pady=10)
        
        self.recommendationLabel = tk.Label(root, text="", font=("Arial", 10), fg="blue")
        self.recommendationLabel.pack(pady=10)

    # 🔹 Core Fatigue Logic
    def analyzeFatigue(self):
        conn = getConnection()
        cursor = conn.cursor()
        
        # Fetch last 7 study sessions for the user
        cursor.execute("""
            SELECT startTime, duration, focusLevel
            FROM studySessions
            WHERE userId = %s
            ORDER BY startTime DESC
            LIMIT 7
        """, (self.userId,))
        
        sessions = cursor.fetchall()
        conn.close()
        
        if not sessions:
            messagebox.showinfo("Info", "No study sessions found.")
            return
        
        # Calculate trends
        focusValues = [row[2] for row in sessions]
        durationValues = [row[1] for row in sessions]
        
        # Simple trend: last - first
        focusTrend = focusValues[-1] - focusValues[0]  # negative => decreasing focus
        durationTrend = durationValues[-1] - durationValues[0]  # positive => increasing duration
        
        # Fatigue logic thresholds (customize as needed)
        focusThreshold = -2  # focus decreased by 2 or more
        durationThreshold = 2  # duration increased by 2 hours or more
        
        fatigueScore = abs(focusTrend) * durationTrend  # simple score calculation
        fatigueAlert = False
        
        if focusTrend < focusThreshold and durationTrend > durationThreshold:
            fatigueAlert = True
            message = f"⚠️ Fatigue Detected! Score: {round(fatigueScore,2)}"
            recommendation = "💡 Take a short break, relax, and avoid long continuous sessions."
        else:
            message = f"✅ Fatigue level normal. Score: {round(fatigueScore,2)}"
            recommendation = "Keep up the good study habits!"
        
        # Display results
        self.resultLabel.config(text=message)
        self.recommendationLabel.config(text=recommendation)
