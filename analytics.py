# analytics_module.py
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from db_connection import getConnection

class AnalyticsModule:

    def __init__(self, root, userId):
        self.root = root
        self.userId = userIqd
        self.root.title("Productivity Analytics")
        self.root.geometry("600x500")

        tk.Label(root, text="Analytics Dashboard", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Button(root, text="Load Dashboard", command=self.loadDashboard).pack(pady=5)
        tk.Button(root, text="Weekly Report", command=self.weeklyReport).pack(pady=5)
        tk.Button(root, text="Monthly Report", command=self.monthlyReport).pack(pady=5)

        self.canvasFrame = tk.Frame(root)
        self.canvasFrame.pack(fill=tk.BOTH, expand=True)

    # 🔹 Fetch aggregated data
    def fetchProductivityData(self):
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                AVG(focusLevel),
                SUM(duration),
                AVG(difficultyLevel)
            FROM studySessions
            WHERE userId = %s
        """, (self.userId,))
        result = cursor.fetchone()
        conn.close()

        # Convert decimal.Decimal to float
        avgFocus = float(result[0]) if result[0] is not None else 0
        totalHours = float(result[1]) if result[1] is not None else 0
        avg_difficulty = float(result[2]) if result[2] is not None else 1

        productivity_score = (avgFocus * totalHours) / avgDifficulty
        return avgFocus, totalHours, productivityScore

    # 🔹 Dashboard Screen
    def loadDashboard(self):
        avgFocus, totalHours, productivityScore = self.fetchProductivityData()
        messagebox.showinfo("Dashboard",
                            f"Average Focus: {round(avgFocus,2)}\n"
                            f"Total Hours: {round(totalHours,2)}\n"
                            f"Productivity Score: {round(productivityScore,2)}")
        self.showBarChart(avgFocus, totalHours, productivityScore)

    # 🔹 Bar Chart
    def showBarChart(self, avgFocus, totalHours, productivityScore):
        for widget in self.canvasFrame.winfoChildren():
            widget.destroy()

        fig, ax = plt.subplots()
        labels = ['Avg Focus', 'Total Hours', 'Productivity']
        values = [avgFocus, totalHours, productivityScore]
        ax.bar(labels, values, color=['blue','green','orange'])
        canvas = FigureCanvasTkAgg(fig, master=self.canvasFrame)
        canvas.draw()
        canvas.getTkWidget().pack()

    # 🔹 Weekly Report
    def weeklyReport(self):
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DAYNAME(startTime), SUM(duration)
            FROM studySessions
            WHERE userId = %s
            GROUP BY DAYNAME(startTime)
        """, (self.user_id,))
        data = cursor.fetchall()
        conn.close()

        if not data:
            messagebox.showinfo("Weekly Report", "No data available for weekly report.")
            return

        days = [row[0] for row in data]
        hours = [float(row[1]) for row in data]  # convert decimal to float

        self.showLineChart(days, hours, "Weekly Study Trend")

    # 🔹 Monthly Report
    def monthlyReport(self):
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT MONTHNAME(startTime), SUM(duration)
            FROM studySessions
            WHERE userId = %s
            GROUP BY MONTHNAME(startTime)
        """, (self.user_id,))
        data = cursor.fetchall()
        conn.close()

        if not data:
            messagebox.showinfo("Monthly Report", "No data available for monthly report.")
            return

        months = [row[0] for row in data]
        hours = [float(row[1]) for row in data]  # convert decimal to float

        self.showLineChart(months, hours, "Monthly Study Trend")

    # 🔹 Line Chart
    def showLineChart(self, labels, values, title):
        for widget in self.canvasFrame.winfoChildren():
            widget.destroy()

        fig, ax = plt.subplots()
        ax.plot(labels, values, marker='o')
        ax.setTitle(title)
        ax.setylabel("Hours")
        canvas = FigureCanvasTkAgg(fig, master=self.canvasFrame)
        canvas.draw()
        canvas.getTkWidget().pack()


# 🔹 Run standalone for testing
if __name__ == "__main__":
    root = tk.Tk()
    userId = int(input("Enter user_id to test Analytics Module: "))
    app = AnalyticsModule(root, userId)
    root.mainloop()
