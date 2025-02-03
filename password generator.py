import tkinter as tk
from tkinter import messagebox
import random
import string
import pyperclip  # To copy password to clipboard

def generate_password():
    try:
        length = int(length_entry.get())
        if length < 4:
            messagebox.showwarning("Warning", "Password length should be at least 4 characters!")
            return
        
        chars = ""
        if letters_var.get():
            chars += string.ascii_letters
        if numbers_var.get():
            chars += string.digits
        if symbols_var.get():
            chars += string.punctuation
        
        if not chars:
            messagebox.showwarning("Warning", "Select at least one option (Letters, Numbers, Symbols)!")
            return

        password = ''.join(random.choice(chars) for _ in range(length))
        password_var.set(password)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number!")

def copy_to_clipboard():
    pyperclip.copy(password_var.get())
    messagebox.showinfo("Copied", "Password copied to clipboard!")

# GUI Setup
root = tk.Tk()
root.title("🔐 Password Generator")
root.geometry("500x400")
root.configure(bg="#222831")

# Title Label
tk.Label(root, text="Advanced Password Generator", font=("Arial", 16, "bold"), fg="white", bg="#222831").pack(pady=10)

# Length Input
tk.Label(root, text="Enter Password Length:", font=("Arial", 12), fg="white", bg="#222831").pack(pady=5)
length_entry = tk.Entry(root, font=("Arial", 12), width=5)
length_entry.pack(pady=5)

# Variables for checkboxes (initialized properly)
letters_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)

# Options Frame
options_frame = tk.Frame(root, bg="#222831")
options_frame.pack(pady=5)

# Checkboxes for password criteria
letters_check = tk.Checkbutton(options_frame, text="Letters", variable=letters_var, font=("Arial", 12), fg="white", bg="#222831", selectcolor="#222831")
letters_check.grid(row=0, column=0)

numbers_check = tk.Checkbutton(options_frame, text="Numbers", variable=numbers_var, font=("Arial", 12), fg="white", bg="#222831", selectcolor="#222831")
numbers_check.grid(row=0, column=1)

symbols_check = tk.Checkbutton(options_frame, text="Symbols", variable=symbols_var, font=("Arial", 12), fg="white", bg="#222831", selectcolor="#222831")
symbols_check.grid(row=0, column=2)

# Generate Button
generate_button = tk.Button(root, text="Generate Password", font=("Arial", 12, "bold"), bg="#00ADB5", fg="white", command=generate_password)
generate_button.pack(pady=15)

# Password Display
password_var = tk.StringVar()
password_entry = tk.Entry(root, textvariable=password_var, font=("Arial", 14), width=30, state="readonly", justify="center", bg="#EEEEEE")
password_entry.pack(pady=5)

# Copy to Clipboard Button
copy_button = tk.Button(root, text="Copy to Clipboard", font=("Arial", 12), bg="#393E46", fg="white", command=copy_to_clipboard)
copy_button.pack(pady=10)

root.mainloop()
