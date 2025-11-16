import tkinter as tk
import random
import os
import time
import threading
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Base path
base = os.path.dirname(os.path.abspath(__file__))

# Play background music in loop
bg_music_path = os.path.join(base, "background.mp3")
pygame.mixer.music.load(bg_music_path)
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(loops=-1)

# Load jokes
def load_jokes():
    jokes = []
    path = os.path.join(base, "randomjokes.txt")
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if "?" in line:
                setup, punchline = line.split("?", 1)
                jokes.append((setup + "?", punchline))
    return jokes

jokes_list = load_jokes()
emoji_list = ["😂", "🤣", "😆", "😹", "🤭"]
current_joke = None

# GUI window
root = tk.Tk()
root.title("🎤 Alexa Joke Assistant 🎤")
root.geometry("600x520")
root.resizable(False, False)

# Aesthetic gradient colors (pastel soft)
gradient_colors = [
    "#ffecd2", "#fcb69f", "#a1c4fd", "#c2e9fb",
    "#d4fc79", "#96e6a1", "#fbc2eb", "#a6c1ee"
]
gradient_index = 0

# Functions
def animate_background():
    global gradient_index
    color = gradient_colors[gradient_index]
    root.config(bg=color)
    heading_label.config(bg=color)
    cat_label.config(bg=color)
    joke_frame.config(bg=color)
    setup_label.config(bg=color)
    punchline_label.config(bg=color)
    emoji_label.config(bg=color)
    btn_frame.config(bg=color)
    gradient_index = (gradient_index + 1) % len(gradient_colors)
    root.after(500, animate_background)

def show_joke():
    global current_joke
    current_joke = random.choice(jokes_list)
    setup_label.config(text=current_joke[0])
    punchline_label.config(text="")
    emoji_label.config(text="")

def play_laugh():
    laugh_path = os.path.join(base, "laugh.mp3")
    try:
        laugh_sound = pygame.mixer.Sound(laugh_path)
        laugh_sound.set_volume(1.0)
        laugh_sound.play()
    except:
        print("Error: could not play laugh sound.")

def show_punchline():
    if current_joke:
        punchline_label.config(text="")
        punchline_text = current_joke[1]
        for i in range(len(punchline_text)+1):
            punchline_label.config(text=punchline_text[:i])
            punchline_label.update()
            time.sleep(0.03)
        threading.Thread(target=play_laugh, daemon=True).start()
        emoji_label.config(text=random.choice(emoji_list))

# Heading label
heading_label = tk.Label(root, text="🎤 Alexa tells me a Joke 🎤",
                         font=("Poppins", 20, "bold"),
                         fg="#333333")
heading_label.pack(pady=(15,5))

# Laughing cat emoji below heading
cat_label = tk.Label(root, text="😹", font=("Arial", 60), bg=gradient_colors[0])
cat_label.pack(pady=(0,10))

# Joke frame
joke_frame = tk.Frame(root)
joke_frame.pack(pady=20)

setup_label = tk.Label(joke_frame, text="", font=("Poppins", 16, "bold"),
                       wraplength=550, justify="center")
setup_label.pack(pady=(0,15))

punchline_label = tk.Label(joke_frame, text="", font=("Poppins", 14, "italic"),
                           fg="#1E90FF", wraplength=550, justify="center")
punchline_label.pack(pady=(0,15))

emoji_label = tk.Label(joke_frame, text="", font=("Arial", 30), justify="center")
emoji_label.pack(pady=(0,15))

# Buttons frame
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

btn_joke = tk.Button(btn_frame, text="🎉 Alexa tell me a Joke", command=show_joke,
                     width=20, bg="#FFB6C1", fg="#333333", font=("Poppins", 12, "bold"), relief="flat")
btn_joke.grid(row=0, column=0, padx=5, pady=5)

btn_punchline = tk.Button(btn_frame, text="😆 Show Punchline", command=show_punchline,
                          width=15, bg="#A1C4FD", fg="#333333", font=("Poppins", 12, "bold"), relief="flat")
btn_punchline.grid(row=0, column=1, padx=5, pady=5)

btn_next = tk.Button(btn_frame, text="➡️ Next Joke", command=show_joke,
                     width=12, bg="#D4FC79", fg="#333333", font=("Poppins", 12, "bold"), relief="flat")
btn_next.grid(row=0, column=2, padx=5, pady=5)

btn_quit = tk.Button(root, text="❌ Quit", command=root.quit,
                     width=10, bg="#FBC2EB", fg="#333333", font=("Poppins", 12, "bold"), relief="flat")
btn_quit.pack(pady=15)

# Start gradient animation
animate_background()

root.mainloop()
