import tkinter as tk
from tkinter import messagebox, simpledialog
from db_connection import get_connection

class SubjectModule:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id

        self.root.title("Subject Management")
        self.root.geometry("500x500")

        tk.Label(root, text="Subject Management", font=("Arial", 14, "bold")).pack(pady=10)

        # Add new subject
        tk.Label(root, text="Subject Name").pack()
        self.entry_subject = tk.Entry(root)
        self.entry_subject.pack(pady=5)
        tk.Button(root, text="Add Subject", command=self.add_subject).pack(pady=5)

        # Subject list
        self.subject_listbox = tk.Listbox(root)
        self.subject_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

        # Buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=5)
        tk.Button(button_frame, text="Delete Selected", command=self.delete_subject).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Edit Name", command=self.edit_subject).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="View Details", command=self.view_subject).grid(row=0, column=2, padx=5)

        self.subject_data = []
        self.load_subjects()

    def load_subjects(self):
        """Load subjects from DB and update listbox with continuous numbering."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT subject_id, subject_name FROM subjects WHERE user_id = %s", (self.user_id,))
            self.subject_data = cursor.fetchall()
            self.subject_listbox.delete(0, tk.END)
            # Display with continuous numbering
            for idx, (subject_id, subject_name) in enumerate(self.subject_data, start=1):
                self.subject_listbox.insert(tk.END, f"{idx} - {subject_name}")
            conn.close()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def add_subject(self):
        name = self.entry_subject.get()
        if not name:
            messagebox.showerror("Error", "Enter subject name")
            return
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO subjects (user_id, subject_name) VALUES (%s, %s)", (self.user_id, name))
            conn.commit()
            conn.close()
            self.entry_subject.delete(0, tk.END)
            self.load_subjects()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def delete_subject(self):
        selected = self.subject_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Select subject to delete")
            return
        try:
            index = selected[0]
            subject_id = self.subject_data[index][0]
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM subjects WHERE subject_id = %s AND user_id = %s", (subject_id, self.user_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Subject Deleted!")
            self.load_subjects()  # numbering will automatically adjust
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def edit_subject(self):
        selected = self.subject_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Select subject to edit")
            return
        index = selected[0]
        subject_id, old_name = self.subject_data[index]
        new_name = simpledialog.askstring("Edit Subject", f"Edit name for '{old_name}':", initialvalue=old_name)
        if new_name:
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE subjects SET subject_name = %s WHERE subject_id = %s AND user_id = %s", (new_name, subject_id, self.user_id))
                conn.commit()
                conn.close()
                self.load_subjects()
            except Exception as e:
                messagebox.showerror("Database Error", str(e))

    def view_subject(self):
        selected = self.subject_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Select subject to view")
            return
        index = selected[0]
        subject_id, subject_name = self.subject_data[index]
        messagebox.showinfo("Subject Details", f"Subject ID: {subject_id}\nName: {subject_name}")
