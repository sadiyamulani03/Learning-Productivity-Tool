# login.py
import tkinter as tk
from tkinter import messagebox
import bcrypt
from db_connection import get_connection
from dashboard import Dashboard

current_user_id = None

# -------- LOGIN FUNCTION --------
def login_user():
    global current_user_id

    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showerror("Error", "Enter username and password")
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT user_id, password_hash FROM users WHERE username = %s",
            (username,)
        )
        result = cursor.fetchone()
        conn.close()

        if result:
            user_id, stored_hash = result
            if isinstance(stored_hash, str):
                stored_hash = stored_hash.encode('utf-8')

            if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                messagebox.showinfo("Success", "Login Successful!")
                current_user_id = user_id

                root.destroy()
                dashboard_root = tk.Tk()
                Dashboard(dashboard_root, current_user_id)
                dashboard_root.mainloop()
            else:
                messagebox.showerror("Error", "Invalid Password")
        else:
            messagebox.showerror("Error", "User not found")

    except Exception as e:
        messagebox.showerror("Database Error", str(e))


# -------- REGISTER FUNCTION --------
def register_user():
    full_name = entry_fullname.get()
    username = entry_username.get()
    email = entry_email.get()
    password = entry_password.get()

    if not full_name or not username or not email or not password:
        messagebox.showerror("Error", "All fields are required for registration!")
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Check if username/email exists
        cursor.execute("SELECT user_id FROM users WHERE username=%s OR email=%s", (username, email))
        if cursor.fetchone():
            messagebox.showerror("Error", "Username or Email already exists!")
            conn.close()
            return

        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        cursor.execute(
            "INSERT INTO users (full_name, username, email, password_hash) VALUES (%s,%s,%s,%s)",
            (full_name, username, email, hashed_password.decode('utf-8'))
        )
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Registration Successful! You can now login.")

        # Clear fields
        entry_fullname.delete(0, tk.END)
        entry_username.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_password.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Database Error", str(e))


# -------- UI --------
root = tk.Tk()
root.title("Learning Productivity Tool")
root.geometry("400x450")

tk.Label(root, text="Welcome", font=("Arial", 16, "bold")).pack(pady=10)

# Full Name (for registration)
tk.Label(root, text="Full Name").pack()
entry_fullname = tk.Entry(root)
entry_fullname.pack(pady=5)

tk.Label(root, text="Email").pack()
entry_email = tk.Entry(root)
entry_email.pack(pady=5)

tk.Label(root, text="Username").pack()
entry_username = tk.Entry(root)
entry_username.pack(pady=5)

tk.Label(root, text="Password").pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=5)

# Buttons
tk.Button(root, text="Login", width=20, command=login_user).pack(pady=10)
tk.Button(root, text="Register", width=20, command=register_user).pack(pady=5)

root.mainloop()
