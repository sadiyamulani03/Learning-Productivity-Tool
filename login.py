# login.py
import tkinter as tk
from tkinter import messagebox
import bcrypt
from db_connection import getConnection
from dashboard import Dashboard

currentUserId = None

# -------- LOGIN FUNCTION --------
def loginUser():
    global currentUserId

    username = entryUsername.get()
    password = entryPassword.get()

    if not username or not password:
        messagebox.showerror("Error", "Enter username and password")
        return

    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT userId, passwordHash FROM users WHERE username = %s",
            (username,)
        )
        result = cursor.fetchone()
        conn.close()

        if result:
            userId, storedHash = result
            if isinstance(storedHash, str):
                storedHash = storedHash.encode('utf-8')

            if bcrypt.checkpw(password.encode('utf-8'), storedHash):
                messagebox.showinfo("Success", "Login Successful!")
                currentUserId = userId

                root.destroy()
                dashboardRoot = tk.Tk()
                Dashboard(dashboardRoot, currentUserId)
                dashboardRoot.mainloop()
            else:
                messagebox.showerror("Error", "Invalid Password")
        else:
            messagebox.showerror("Error", "User not found")

    except Exception as e:
        messagebox.showerror("Database Error", str(e))


# -------- REGISTER FUNCTION --------
def registerUser():
    fullName = entryFullname.get()
    username = entryUsername.get()
    email = entryEmail.get()
    password = entryPassword.get()

    if not fullName or not username or not email or not password:
        messagebox.showerror("Error", "All fields are required for registration!")
        return

    try:
        conn = getConnection()
        cursor = conn.cursor()
        # Check if username/email exists
        cursor.execute("SELECT user_id FROM users WHERE username=%s OR email=%s", (username, email))
        if cursor.fetchone():
            messagebox.showerror("Error", "Username or Email already exists!")
            conn.close()
            return

        # Hash password
        hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        cursor.execute(
            "INSERT INTO users (full_name, username, email, password_hash) VALUES (%s,%s,%s,%s)",
            (fullName, username, email, hashedPassword.decode('utf-8'))
        )
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Registration Successful! You can now login.")

        # Clear fields
        entryFullname.delete(0, tk.END)
        entryUsername.delete(0, tk.END)
        entryEmail.delete(0, tk.END)
        entryPassword.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Database Error", str(e))


# -------- UI --------
root = tk.Tk()
root.title("Learning Productivity Tool")
root.geometry("400x450")

tk.Label(root, text="Welcome", font=("Arial", 16, "bold")).pack(pady=10)

# Full Name (for registration)
tk.Label(root, text="Full Name").pack()
entryFullname = tk.Entry(root)
entryFullname.pack(pady=5)

tk.Label(root, text="Email").pack()
entryEmail = tk.Entry(root)
entryEmail.pack(pady=5)

tk.Label(root, text="Username").pack()
entryUsername = tk.Entry(root)
entryUsername.pack(pady=5)

tk.Label(root, text="Password").pack()
entryPassword = tk.Entry(root, show="*")
entryPassword.pack(pady=5)

# Buttons
tk.Button(root, text="Login", width=20, command=loginUser).pack(pady=10)
tk.Button(root, text="Register", width=20, command=registerUser).pack(pady=5)

root.mainloop()
