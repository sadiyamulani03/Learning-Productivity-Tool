# analytics_module.py
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from db_connection import get_connection

class AnalyticsModule:

    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.root.title("Productivity Analytics")
        self.root.geometry("600x500")

        tk.Label(root, text="Analytics Dashboard", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Button(root, text="Load Dashboard", command=self.load_dashboard).pack(pady=5)
        tk.Button(root, text="Weekly Report", command=self.weekly_report).pack(pady=5)
        tk.Button(root, text="Monthly Report", command=self.monthly_report).pack(pady=5)

        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

    # 🔹 Fetch aggregated data
    def fetch_productivity_data(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                AVG(focus_level),
                SUM(duration),
                AVG(difficulty_level)
            FROM study_sessions
            WHERE user_id = %s
        """, (self.user_id,))
        result = cursor.fetchone()
        conn.close()

        # Convert decimal.Decimal to float
        avg_focus = float(result[0]) if result[0] is not None else 0
        total_hours = float(result[1]) if result[1] is not None else 0
        avg_difficulty = float(result[2]) if result[2] is not None else 1

        productivity_score = (avg_focus * total_hours) / avg_difficulty
        return avg_focus, total_hours, productivity_score

    # 🔹 Dashboard Screen
    def load_dashboard(self):
        avg_focus, total_hours, productivity_score = self.fetch_productivity_data()
        messagebox.showinfo("Dashboard",
                            f"Average Focus: {round(avg_focus,2)}\n"
                            f"Total Hours: {round(total_hours,2)}\n"
                            f"Productivity Score: {round(productivity_score,2)}")
        self.show_bar_chart(avg_focus, total_hours, productivity_score)

    # 🔹 Bar Chart
    def show_bar_chart(self, avg_focus, total_hours, productivity_score):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots()
        labels = ['Avg Focus', 'Total Hours', 'Productivity']
        values = [avg_focus, total_hours, productivity_score]
        ax.bar(labels, values, color=['blue','green','orange'])
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    # 🔹 Weekly Report
    def weekly_report(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DAYNAME(start_time), SUM(duration)
            FROM study_sessions
            WHERE user_id = %s
            GROUP BY DAYNAME(start_time)
        """, (self.user_id,))
        data = cursor.fetchall()
        conn.close()

        if not data:
            messagebox.showinfo("Weekly Report", "No data available for weekly report.")
            return

        days = [row[0] for row in data]
        hours = [float(row[1]) for row in data]  # convert decimal to float

        self.show_line_chart(days, hours, "Weekly Study Trend")

    # 🔹 Monthly Report
    def monthly_report(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT MONTHNAME(start_time), SUM(duration)
            FROM study_sessions
            WHERE user_id = %s
            GROUP BY MONTHNAME(start_time)
        """, (self.user_id,))
        data = cursor.fetchall()
        conn.close()

        if not data:
            messagebox.showinfo("Monthly Report", "No data available for monthly report.")
            return

        months = [row[0] for row in data]
        hours = [float(row[1]) for row in data]  # convert decimal to float

        self.show_line_chart(months, hours, "Monthly Study Trend")

    # 🔹 Line Chart
    def show_line_chart(self, labels, values, title):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots()
        ax.plot(labels, values, marker='o')
        ax.set_title(title)
        ax.set_ylabel("Hours")
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()


# 🔹 Run standalone for testing
if __name__ == "__main__":
    root = tk.Tk()
    user_id = int(input("Enter user_id to test Analytics Module: "))
    app = AnalyticsModule(root, user_id)
    root.mainloop()
