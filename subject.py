import tkinter as tk
from tkinter import messagebox, simpledialog
from db_connection import getConnection

class SubjectModule:
    def __init__(self, root, userId):
        self.root = root
        self.userId = userId

        self.root.title("Subject Management")
        self.root.geometry("500x500")

        tk.Label(root, text="Subject Management", font=("Arial", 14, "bold")).pack(pady=10)

        # Add new subject
        tk.Label(root, text="Subject Name").pack()
        self.entrySubject = tk.Entry(root)
        self.entrySubject.pack(pady=5)
        tk.Button(root, text="Add Subject", command=self.addSubject).pack(pady=5)

        # Subject list
        self.subjectListbox = tk.Listbox(root)
        self.subjectListbox.pack(pady=10, fill=tk.BOTH, expand=True)

        # Buttons
        buttonFrame = tk.Frame(root)
        buttonFrame.pack(pady=5)
        tk.Button(buttonFrame, text="Delete Selected", command=self.deleteSubject).grid(row=0, column=0, padx=5)
        tk.Button(buttonFrame, text="Edit Name", command=self.editSubject).grid(row=0, column=1, padx=5)
        tk.Button(buttonFrame, text="View Details", command=self.viewSubject).grid(row=0, column=2, padx=5)

        self.subjectData = []
        self.loadSubjects()

    def loadSubjects(self):
        """Load subjects from DB and update listbox with continuous numbering."""
        try:
            conn = getConnection()
            cursor = conn.cursor()
            cursor.execute("SELECT subjectId, subjectName FROM subjects WHERE userId = %s", (self.userId,))
            self.subjectData = cursor.fetchall()
            self.subjectListbox.delete(0, tk.END)
            # Display with continuous numbering
            for idx, (subjectId, subjectName) in enumerate(self.subjectData, start=1):
                self.subjectListbox.insert(tk.END, f"{idx} - {subjectName}")
            conn.close()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def addSubject(self):
        name = self.entrySubject.get()
        if not name:
            messagebox.showerror("Error", "Enter subject name")
            return
        try:
            conn = getConnection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO subjects (userId, subjectName) VALUES (%s, %s)", (self.userId, name))
            conn.commit()
            conn.close()
            self.entrySubject.delete(0, tk.END)
            self.loadSubjects()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def deleteSubject(self):
        selected = self.subjectListbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Select subject to delete")
            return
        try:
            index = selected[0]
            subjectId = self.subjectData[index][0]
            conn = getConnection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM subjects WHERE subjectId = %s AND userId = %s", (subjectId, self.userId))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Subject Deleted!")
            self.loadSubjects()  # numbering will automatically adjust
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def editSubject(self):
        selected = self.subjectListbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Select subject to edit")
            return
        index = selected[0]
        subjectId, oldName = self.subjectData[index]
        newName = simpledialog.askstring("Edit Subject", f"Edit name for '{oldName}':", initialvalue=oldName)
        if newName:
            try:
                conn = getConnection()
                cursor = conn.cursor()
                cursor.execute("UPDATE subjects SET subjectName = %s WHERE subjectId = %s AND userId = %s", (newName, subjectId, self.userId))
                conn.commit()
                conn.close()
                self.loadSubjects()
            except Exception as e:
                messagebox.showerror("Database Error", str(e))

    def viewSubject(self):
        selected = self.subjectListbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Select subject to view")
            return
        index = selected[0]
        subjectId, subjectName = self.subjectData[index]
        messagebox.showinfo("Subject Details", f"Subject ID: {subjectId}\nName: {subjectName}")
