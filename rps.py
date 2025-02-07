import random
import tkinter as tk
from tkinter import messagebox

def play(user_choice):
    choices = ["Rock", "Paper", "Scissors"]
    computer_choice = random.choice(choices)
    
    result = determine_winner(user_choice, computer_choice)
    result_label.config(text=f"Computer chose {computer_choice}\n{result}")
    
    update_score(result)

def determine_winner(user, computer):
    if user == computer:
        return "It's a Tie!"
    elif (user == "Rock" and computer == "Scissors") or \
         (user == "Scissors" and computer == "Paper") or \
         (user == "Paper" and computer == "Rock"):
        return "You Win!"
    else:
        return "You Lose!"

def update_score(result):
    global user_score, computer_score
    if "Win" in result:
        user_score += 1
    elif "Lose" in result:
        computer_score += 1
    score_label.config(text=f"Score - You: {user_score} | Computer: {computer_score}")

def reset_game():
    global user_score, computer_score
    user_score, computer_score = 0, 0
    result_label.config(text="")
    score_label.config(text="Score - You: 0 | Computer: 0")

def exit_game():
    root.destroy()

# GUI Setup
root = tk.Tk()
root.title("Rock-Paper-Scissors Game")
root.geometry("400x400")
root.configure(bg="#f0f0f0")

user_score, computer_score = 0, 0

title_label = tk.Label(root, text="Rock-Paper-Scissors", font=("Arial", 20, "bold"), bg="#f0f0f0")
title_label.pack(pady=10)

button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack()

for choice in ["Rock", "Paper", "Scissors"]:
    tk.Button(button_frame, text=choice, font=("Arial", 12), command=lambda c=choice: play(c), bg="#ffffff", width=10).pack(side=tk.LEFT, padx=10)

result_label = tk.Label(root, text="", font=("Arial", 14), bg="#f0f0f0")
result_label.pack(pady=20)

score_label = tk.Label(root, text="Score - You: 0 | Computer: 0", font=("Arial", 14), bg="#f0f0f0")
score_label.pack()

button_frame_2 = tk.Frame(root, bg="#f0f0f0")
button_frame_2.pack(pady=10)

reset_button = tk.Button(button_frame_2, text="Reset", font=("Arial", 12), command=reset_game, bg="#ffcc00", fg="black", width=10)
reset_button.pack(side=tk.LEFT, padx=10)

exit_button = tk.Button(button_frame_2, text="Exit", font=("Arial", 12), command=exit_game, bg="#ff3333", fg="white", width=10)
exit_button.pack(side=tk.LEFT, padx=10)

root.mainloop()
