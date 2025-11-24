import tkinter as tk
from tkinter import messagebox
import random
import pygame
from PIL import Image, ImageTk
import os

# -------------------- Root Window --------------------
root = tk.Tk()
root.title("🌈 Math Quiz 🌈")
root.geometry("700x500")
root.config(bg="#ffe6f2")

# -------------------- Setup pygame --------------------
pygame.mixer.init()
pygame.mixer.music.load("Bgm.mp3")
pygame.mixer.music.play(-1)

ding_sound = "ding.mp3"
buzzer_sound = "buzzer.mp3"

# Global variables
score = 0
high_score = 0
question_number = 0
difficulty = None
cute_img_label = None
asked_questions = []
current_question = None
first_try = True

# -------------------- Load Images --------------------
try:
    img = Image.open("cute_character.png").resize((120, 120))
    cute_img = ImageTk.PhotoImage(img)
except:
    cute_img = None

try:
    left_image = Image.open("left_img.jpg").resize((80, 80))
    left_img = ImageTk.PhotoImage(left_image)
except:
    left_img = None

try:
    right_image = Image.open("right_img.jpg").resize((80, 80))
    right_img = ImageTk.PhotoImage(right_image)
except:
    right_img = None

# Load high score
if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as f:
        try:
            high_score = int(f.read())
        except:
            high_score = 0

# -------------------- Helper Functions --------------------
def randomInt(min_val, max_val):
    return random.randint(min_val, max_val)

def decideOperation():
    return random.choice(["+", "-"])

def play_sound(file):
    pygame.mixer.Sound(file).play()

def jump_character(widget):
    def jump(step):
        if step < 6:
            widget.place_configure(y=widget.winfo_y() - 5 if step % 2 == 0 else widget.winfo_y() + 5)
            root.after(100, lambda: jump(step + 1))
    jump(0)

def shake_character(widget):
    orig_x = widget.winfo_x()
    def shake(step):
        if step < 6:
            widget.place_configure(x=orig_x + (-10 if step % 2 == 0 else 10))
            root.after(100, lambda: shake(step + 1))
        else:
            widget.place_configure(x=orig_x)
    shake(0)

# -------------------- Floating Effects --------------------
def float_points(points):
    """Floating +10 or +5 above the cute character"""
    if not cute_img_label:
        return
    x = cute_img_label.winfo_x() + 40
    y = cute_img_label.winfo_y() - 20
    lbl = tk.Label(root, text=f"+{points}", font=("Comic Sans MS", 18, "bold"), fg="gold", bg="#e6f7ff")
    lbl.place(x=x, y=y)

    def move(step):
        if step < 20:
            lbl.place(y=y - step*3)
            root.after(50, lambda: move(step+1))
        else:
            lbl.destroy()
    move(0)

def confetti_effect():
    colors = ["#ff4d4d","#66b3ff","#99ff99","#ffcc99","#ff99ff","#ffff99"]
    for i in range(30):
        piece = tk.Label(root, text="🎊", font=("Arial", 14),
                         fg=random.choice(colors), bg="#e6f7ff")
        piece.place(x=random.randint(0, 700), y=random.randint(0, 500))
        move_confetti(piece, 0)

def move_confetti(widget, step):
    if step < 20:
        widget.place(y=widget.winfo_y() + 10)
        root.after(50, lambda: move_confetti(widget, step+1))
    else:
        widget.destroy()

# -------------------- Score Update --------------------
def updateScore(points):
    global score
    score += points
    score_label.config(text=f"Score: {score}")
    float_points(points)
    confetti_effect()
    play_sound(ding_sound)
    if cute_img_label:
        jump_character(cute_img_label)

def nextQuestion():
    global question_number, first_try
    question_number += 1
    first_try = True
    displayProblem()

def displayResults():
    global high_score, asked_questions
    grade = ""
    if score >= 90:
        grade = "A+ 🌟"
    elif score >= 75:
        grade = "A 💫"
    elif score >= 60:
        grade = "B 👍"
    elif score >= 40:
        grade = "C 😊"
    else:
        grade = "Needs Practice 💪"

    if score > high_score:
        high_score = score
        with open("highscore.txt", "w") as f:
            f.write(str(high_score))

    messagebox.showinfo("Quiz Complete 🎊",
                        f"Your score: {score}/100\nGrade: {grade}\nHigh Score: {high_score}")

    play_again = messagebox.askyesno("Play Again?", "Would you like to play again?")
    if play_again:
        asked_questions = []
        displayMenu()
    else:
        root.destroy()

# -------------------- Quiz Logic --------------------
def displayProblem():
    global question_number, first_try, current_question, asked_questions

    if question_number >= 10:
        displayResults()
        return

    question_number_label.config(text=f"Question {question_number+1} of 10")

    # Generate a unique random question only if it's the first try
    if first_try:
        while True:
            if difficulty == "Easy":
                a = randomInt(1, 9)
                b = randomInt(1, 9)
            elif difficulty == "Moderate":
                a = randomInt(10, 99)
                b = randomInt(10, 99)
            else:
                a = randomInt(1000, 9999)
                b = randomInt(1000, 9999)
            op = decideOperation()
            correct_answer = a + b if op == "+" else a - b
            question_tuple = (a, op, b)
            if question_tuple not in asked_questions:
                asked_questions.append(question_tuple)
                break
        current_question = {"a": a, "b": b, "op": op, "answer": correct_answer}

    question_label.config(text=f"{current_question['a']} {current_question['op']} {current_question['b']} = ?")
    answer_entry.delete(0, tk.END)

    def check_answer():
        global first_try
        user_input = answer_entry.get().strip()
        if not user_input:
            messagebox.showerror("Error", "Please enter a number.")
            return

        if not user_input.isdigit() and not (user_input.startswith('-') and user_input[1:].isdigit()):
            messagebox.showerror("Error", "Please enter a valid integer number.")
            return

        user_answer = int(user_input)

        if user_answer == current_question["answer"]:
            points = 10 if first_try else 5
            updateScore(points)
            messagebox.showinfo("Correct 🎉", f"Correct! You earned {points} points 🌟")
            nextQuestion()
        else:
            if first_try:
                first_try = False
                play_sound(buzzer_sound)
                if cute_img_label:
                    shake_character(cute_img_label)
                messagebox.showwarning("Try Again 💭", "Wrong! Try this question one more time 🌈")
                answer_entry.delete(0, tk.END)
            else:
                play_sound(buzzer_sound)
                messagebox.showinfo("Next Question", "Moving to the next question 🌈")
                nextQuestion()

    submit_btn.config(command=check_answer)

# -------------------- Menu & Start --------------------
def displayMenu():
    global difficulty, score, question_number, cute_img_label, asked_questions
    for widget in root.winfo_children():
        widget.destroy()

    root.config(bg="#ffccff")
    
    if left_img:
        tk.Label(root, image=left_img, bg="#ffccff").place(relx=0.05, rely=0.5, anchor="center")
    if right_img:
        tk.Label(root, image=right_img, bg="#ffccff").place(relx=0.95, rely=0.5, anchor="center")

    title = tk.Label(root, text="🎀 Math Quiz 🎀", font=("Comic Sans MS", 28, "bold"),
                     bg="#ffccff", fg="#660066")
    title.pack(pady=(20,5))

    if cute_img:
        cute_img_label = tk.Label(root, image=cute_img, bg="#ffccff")
        cute_img_label.image = cute_img
        cute_img_label.pack(pady=(0,20))

    tk.Label(root, text=f"High Score: {high_score}", font=("Comic Sans MS", 18),
             bg="#ffccff", fg="#003366").pack(pady=5)

    tk.Label(root, text="Select Difficulty Level 💫", font=("Comic Sans MS", 18),
             bg="#ffccff", fg="#003366").pack(pady=10)

    def set_level(level):
        global difficulty, score, question_number, asked_questions
        difficulty = level
        score = 0
        question_number = 0
        asked_questions = []
        startQuiz(level)

    tk.Button(root, text="Easy 🌸", command=lambda: set_level("Easy"),
              font=("Comic Sans MS", 16, "bold"), bg="#ff99c2", fg="white", width=12).pack(pady=5)
    tk.Button(root, text="Moderate 🌼", command=lambda: set_level("Moderate"),
              font=("Comic Sans MS", 16, "bold"), bg="#ffcc66", fg="white", width=12).pack(pady=5)
    tk.Button(root, text="Advanced 🌺", command=lambda: set_level("Advanced"),
              font=("Comic Sans MS", 16, "bold"), bg="#66ccff", fg="white", width=12).pack(pady=5)

def startQuiz(level):
    global difficulty, cute_img_label, score_label
    difficulty = level
    for widget in root.winfo_children():
        widget.destroy()

    root.config(bg="#e6f7ff")
    tk.Label(root, text=f"{level} Level ✨", font=("Comic Sans MS", 22, "bold"),
             bg="#e6f7ff", fg="#004466").pack(pady=10)
    
    if cute_img:
        cute_img_label = tk.Label(root, image=cute_img, bg="#e6f7ff")
        cute_img_label.image = cute_img
        cute_img_label.pack()

    global question_number_label, question_label, answer_entry, submit_btn
    question_number_label = tk.Label(root, text="", font=("Comic Sans MS", 16), bg="#e6f7ff", fg="#333333")
    question_number_label.pack()

    question_label = tk.Label(root, text="", font=("Comic Sans MS", 24, "bold"), bg="#e6f7ff", fg="#006699")
    question_label.pack(pady=20)

    answer_entry = tk.Entry(root, font=("Comic Sans MS", 18), justify="center")
    answer_entry.pack(pady=10)

    submit_btn = tk.Button(root, text="Submit 💖", font=("Comic Sans MS", 16, "bold"),
                           bg="#99ffcc", fg="#004d00", width=10)
    submit_btn.pack(pady=15)

    score_label = tk.Label(root, text=f"Score: {score}", font=("Comic Sans MS", 18), bg="#e6f7ff", fg="#333333")
    score_label.pack(pady=5)

    displayProblem()

# -------------------- Splash Screen --------------------
def splashScreen():
    splash = tk.Toplevel()
    splash.geometry("700x500")
    splash.overrideredirect(True)
    splash.config(bg="#ffe6f2")

    tk.Label(splash, text="✨ Math Quiz ✨", font=("Comic Sans MS", 32, "bold"),
             fg="#660066", bg="#ffe6f2").pack(expand=True)

    splash.after(2000, lambda: [splash.destroy(), displayMenu()])

splashScreen()
root.mainloop()
