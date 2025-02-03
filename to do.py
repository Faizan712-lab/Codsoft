import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from datetime import datetime

def add_task():
    task = task_entry.get()
    if task.strip():
        date_time = simpledialog.askstring("Input", "Enter due date and time (YYYY-MM-DD HH:MM):")
        try:
            datetime.strptime(date_time, "%Y-%m-%d %H:%M")
            task_with_time = f"{task} | {date_time}"
            task_listbox.insert(tk.END, task_with_time)
            update_task_colors()
            task_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showwarning("Warning", "Invalid date/time format!")
    else:
        messagebox.showwarning("Warning", "Task cannot be empty!")

def remove_task():
    try:
        selected_task_index = task_listbox.curselection()[0]
        task_listbox.delete(selected_task_index)
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to remove!")

def save_tasks():
    tasks = task_listbox.get(0, tk.END)
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            for task in tasks:
                file.write(task + "\n")
        messagebox.showinfo("Success", "Tasks saved successfully!")

def load_tasks():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        task_listbox.delete(0, tk.END)
        with open(file_path, "r") as file:
            for line in file:
                task_listbox.insert(tk.END, line.strip())
        update_task_colors()

def clear_tasks():
    task_listbox.delete(0, tk.END)

def mark_done():
    try:
        selected_task_index = task_listbox.curselection()[0]
        task = task_listbox.get(selected_task_index)
        task_listbox.delete(selected_task_index)
        task_listbox.insert(selected_task_index, f"✔ {task}")
        update_task_colors()
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to mark as done!")

def update_task_colors():
    for i in range(task_listbox.size()):
        task = task_listbox.get(i)
        if "✔" in task:
            task_listbox.itemconfig(i, {'fg': 'green'})
        else:
            task_listbox.itemconfig(i, {'fg': 'red'})

# GUI Setup
root = tk.Tk()
root.title("Advanced To-Do List")
root.geometry("500x500")
root.configure(bg="#f0f0f0")

frame = tk.Frame(root)
frame.pack(pady=10)

task_entry = tk.Entry(frame, width=40)
task_entry.pack(side=tk.LEFT, padx=5)

add_button = tk.Button(frame, text="Add Task", command=add_task)
add_button.pack(side=tk.RIGHT)

task_listbox = tk.Listbox(root, width=60, height=15, bg="#e6e6e6", selectbackground="#a1a1a1")
task_listbox.pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack(pady=5)

remove_button = tk.Button(button_frame, text="Remove Task", command=remove_task)
remove_button.grid(row=0, column=0, padx=5)

mark_done_button = tk.Button(button_frame, text="Mark Done", command=mark_done)
mark_done_button.grid(row=0, column=1, padx=5)

save_button = tk.Button(button_frame, text="Save Tasks", command=save_tasks)
save_button.grid(row=1, column=0, padx=5, pady=5)

load_button = tk.Button(button_frame, text="Load Tasks", command=load_tasks)
load_button.grid(row=1, column=1, padx=5, pady=5)

clear_button = tk.Button(root, text="Clear All", command=clear_tasks)
clear_button.pack(pady=5)

root.mainloop()