import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database Setup
conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        completed BOOLEAN NOT NULL CHECK (completed IN (0, 1))
    )
""")
conn.commit()

# Function to Add Task
def add_task():
    task = task_entry.get()
    if task:
        cursor.execute("INSERT INTO tasks (task, completed) VALUES (?, 0)", (task,))
        conn.commit()
        task_entry.delete(0, tk.END)
        load_tasks()
    else:
        messagebox.showwarning("Warning", "Task cannot be empty!")

# Function to Load Tasks
def load_tasks():
    task_list.delete(0, tk.END)
    cursor.execute("SELECT * FROM tasks")
    for task in cursor.fetchall():
        status = "✅" if task[2] else "❌"
        task_list.insert(tk.END, f"{task[0]}. {status} {task[1]}")

# Function to Mark Task as Completed
def complete_task():
    selected = task_list.curselection()
    if selected:
        task_id = task_list.get(selected[0]).split(".")[0]
        cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
        conn.commit()
        load_tasks()
    else:
        messagebox.showwarning("Warning", "Select a task to complete!")

# Function to Delete Task
def delete_task():
    selected = task_list.curselection()
    if selected:
        task_id = task_list.get(selected[0]).split(".")[0]
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        load_tasks()
    else:
        messagebox.showwarning("Warning", "Select a task to delete!")

# GUI Setup
root = tk.Tk()
root.title("Task Manager")

# Input Field
task_entry = tk.Entry(root, width=40)
task_entry.pack(pady=10)

# Buttons
tk.Button(root, text="Add Task", command=add_task).pack(pady=5)
tk.Button(root, text="Mark as Completed", command=complete_task).pack(pady=5)
tk.Button(root, text="Delete Task", command=delete_task).pack(pady=5)

# Task List
task_list = tk.Listbox(root, width=50)
task_list.pack(pady=10)

# Load Tasks on Startup
load_tasks()

# Run GUI
root.mainloop()

# Close DB Connection on Exit
conn.close()
