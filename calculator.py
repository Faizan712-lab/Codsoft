import tkinter as tk
from tkinter import messagebox

def calculate():
    try:
        num1 = float(entry_num1.get())
        num2 = float(entry_num2.get())
        operation = operation_var.get()
        
        if operation == "+":
            result.set(num1 + num2)
        elif operation == "-":
            result.set(num1 - num2)
        elif operation == "*":
            result.set(num1 * num2)
        elif operation == "/":
            if num2 == 0:
                messagebox.showerror("Error", "Cannot divide by zero!")
                return
            result.set(num1 / num2)
        else:
            messagebox.showerror("Error", "Invalid Operation")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers")

# GUI setup
root = tk.Tk()
root.title("Simple Calculator")
root.geometry("300x300")
root.configure(bg="#f0f0f0")

tk.Label(root, text="Enter First Number:", bg="#f0f0f0").pack(pady=5)
entry_num1 = tk.Entry(root)
entry_num1.pack(pady=5)

tk.Label(root, text="Enter Second Number:", bg="#f0f0f0").pack(pady=5)
entry_num2 = tk.Entry(root)
entry_num2.pack(pady=5)

tk.Label(root, text="Choose Operation:", bg="#f0f0f0").pack(pady=5)
operation_var = tk.StringVar(value="+")
operations = ["+", "-", "*", "/"]
for op in operations:
    tk.Radiobutton(root, text=op, variable=operation_var, value=op, bg="#f0f0f0").pack()

tk.Button(root, text="Calculate", command=calculate, bg="#4CAF50", fg="white").pack(pady=10)

result = tk.StringVar()
tk.Label(root, text="Result:", bg="#f0f0f0").pack(pady=5)
tk.Entry(root, textvariable=result, state='readonly').pack(pady=5)

root.mainloop()
