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
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)  # Loop forever

ding_sound = "ding.mp3"
buzzer_sound = "buzzer.mp3"

# Global variables
score = 0
high_score = 0
question_number = 0
difficulty = None
first_try = True
cute_img_label = None  # Will hold label for animation

# -------------------- Load Images --------------------
try:
    img = Image.open("cute_character.png").resize((120, 120))
    cute_img = ImageTk.PhotoImage(img)
    print("Central image loaded ✅")
except Exception as e:
    cute_img = None
    print("Central image NOT loaded ❌", e)

# Left and Right side images
try:
    left_image = Image.open("left_img.jpg").resize((80, 80))
    left_img = ImageTk.PhotoImage(left_image)
    print("Left image loaded ✅")
except:
    left_img = None
    print("Left image NOT loaded ❌")

try:
    right_image = Image.open("right_img.jpg").resize((80, 80))
    right_img = ImageTk.PhotoImage(right_image)
    print("Right image loaded ✅")
except:
    right_img = None
    print("Right image NOT loaded ❌")

# Load high score if exists
if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as f:
        try:
            high_score = int(f.read())
        except:
            high_score = 0

# -------------------- Floating Animation --------------------
def float_emojis():
    emojis = ["💖", "✨", "⭐", "🎉", "😍"]
    for i in range(10):
        emoji = tk.Label(root, text=random.choice(emojis), font=("Arial", 20),
                         bg=random.choice(["#ffe6f2","#e6f7ff","#fff5e6"]))
        emoji.place(x=random.randint(50, 650), y=400)
        move_emoji(emoji, 0)

def move_emoji(widget, step):
    if step < 30:
        widget.place(y=400 - step*10)
        root.after(50, lambda: move_emoji(widget, step+1))
    else:
        widget.destroy()

# Confetti effect
def confetti_effect():
    colors = ["#ff4d4d","#66b3ff","#99ff99","#ffcc99","#ff99ff","#ffff99"]
    for i in range(50):
        piece = tk.Label(root, text="🎊", font=("Arial", 14),
                         fg=random.choice(colors), bg=random.choice(colors))
        piece.place(x=random.randint(0, 700), y=random.randint(0, 500))
        move_confetti(piece, 0)

def move_confetti(widget, step):
    if step < 20:
        widget.place(y=widget.winfo_y() + 10)
        root.after(50, lambda: move_confetti(widget, step+1))
    else:
        widget.destroy()

# -------------------- Quiz Functions --------------------
def randomInt(min_val, max_val):
    return random.randint(min_val, max_val)

def decideOperation():
    return random.choice(["+", "-"])

def play_sound(file):
    pygame.mixer.Sound(file).play()

# Animations for cute character
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

def isCorrect(user_answer, correct_answer):
    global score, first_try
    if user_answer == correct_answer:
        if first_try:
            score += 10
        else:
            score += 5
        float_emojis()
        play_sound(ding_sound)
        if cute_img_label:
            jump_character(cute_img_label)
        messagebox.showinfo("Correct 🎉", "Yay! That’s right 💖⭐")
        return True
    else:
        if first_try:
            first_try = False
            play_sound(buzzer_sound)
            if cute_img_label:
                shake_character(cute_img_label)
            messagebox.showwarning("Try Again 💭", "Oops! Try once more 🌈")
        else:
            play_sound(buzzer_sound)
            if cute_img_label:
                shake_character(cute_img_label)
            messagebox.showerror("Wrong ❌", f"Answer was {correct_answer}")
        return False

def displayResults():
    global high_score
    confetti_effect()
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
        displayMenu()
    else:
        root.destroy()

def displayProblem():
    global question_number, first_try
    first_try = True

    if question_number >= 10:
        displayResults()
        return

    question_number_label.config(text=f"Question {question_number+1} of 10")

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

    question_label.config(text=f"{a} {op} {b} = ?")
    answer_entry.delete(0, tk.END)

    def check_answer():
        try:
            user_answer = int(answer_entry.get())
            correct = isCorrect(user_answer, correct_answer)
            if correct:
                nextQuestion()
        except:
            messagebox.showerror("Error", "Please enter a valid number.")

    submit_btn.config(command=check_answer)

def nextQuestion():
    global question_number
    question_number += 1
    displayProblem()

# -------------------- Menu & Start --------------------
def displayMenu():
    global difficulty, score, question_number, cute_img_label
    for widget in root.winfo_children():
        widget.destroy()

    root.config(bg="#ffccff")
    
    # Side images
    if left_img:
        tk.Label(root, image=left_img, bg="#ffccff").place(relx=0.05, rely=0.5, anchor="center")
    if right_img:
        tk.Label(root, image=right_img, bg="#ffccff").place(relx=0.95, rely=0.5, anchor="center")

    # Title
    title = tk.Label(root, text="🎀 Math Quiz 🎀", font=("Comic Sans MS", 28, "bold"),
                     bg="#ffccff", fg="#660066")
    title.pack(pady=(20,5))

    # Central cute image
    if cute_img:
        cute_img_label = tk.Label(root, image=cute_img, bg="#ffccff")
        cute_img_label.image = cute_img
        cute_img_label.pack(pady=(0,20))

    tk.Label(root, text=f"High Score: {high_score}", font=("Comic Sans MS", 18),
             bg="#ffccff", fg="#003366").pack(pady=5)

    tk.Label(root, text="Select Difficulty Level 💫", font=("Comic Sans MS", 18),
             bg="#ffccff", fg="#003366").pack(pady=10)

    def set_level(level):
        global difficulty, score, question_number
        difficulty = level
        score = 0
        question_number = 0
        startQuiz(level)

    tk.Button(root, text="Easy 🌸", command=lambda: set_level("Easy"),
              font=("Comic Sans MS", 16, "bold"), bg="#ff99c2", fg="white", width=12).pack(pady=5)
    tk.Button(root, text="Moderate 🌼", command=lambda: set_level("Moderate"),
              font=("Comic Sans MS", 16, "bold"), bg="#ffcc66", fg="white", width=12).pack(pady=5)
    tk.Button(root, text="Advanced 🌺", command=lambda: set_level("Advanced"),
              font=("Comic Sans MS", 16, "bold"), bg="#66ccff", fg="white", width=12).pack(pady=5)

def startQuiz(level):
    global difficulty, cute_img_label
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
