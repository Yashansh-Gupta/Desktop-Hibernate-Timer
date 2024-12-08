import os
import time
import threading
import tkinter as tk
from tkinter import ttk

def hibernate_after(minutes):
    def hibernate():
        global remaining_time, total_time
        total_time = minutes * 60
        for remaining in range(total_time, 0, -1):
            remaining_time = remaining
            if cancel_event.is_set():
                update_status("Hibernation canceled.")
                return
            update_status(f"Time remaining: {remaining // 60} minutes {remaining % 60} seconds")
            time.sleep(1)
        os.system("shutdown /h")

    cancel_event = threading.Event()
    hibernate_thread = threading.Thread(target=hibernate)
    hibernate_thread.start()

    return cancel_event

def update_status(message):
    status_label.config(text=message)

def start_hibernation():
    minutes = int(entry.get())
    global cancel_event
    cancel_event = hibernate_after(minutes)
    start_button.config(state=tk.DISABLED)
    cancel_button.config(state=tk.NORMAL)
    animate_button(start_button)
    animation_thread = threading.Thread(target=smooth_moon_animation, args=(cancel_event,))
    animation_thread.start()

def cancel_hibernation():
    cancel_event.set()
    start_button.config(state=tk.NORMAL)
    cancel_button.config(state=tk.DISABLED)

def animate_button(button):
    original_color = button.cget("bg")
    animation_duration = 1  # seconds
    frames = 60 * animation_duration
    for i in range(frames):
        button.after(int(i * (1000 / 60)), lambda: button.config(bg="#A3BE8C"))
        button.after(int(i * (1000 / 60)) + int((1000 / 60) / 2), lambda: button.config(bg=original_color))

def update_moon_animation(remaining, total):
    canvas.delete("all")
    phase = (remaining / total) * 360  # Gradually reduce the moon
    canvas.create_oval(20, 20, 80, 80, fill="#2E3440", outline="#D8DEE9")
    canvas.create_arc(20, 20, 80, 80, start=90, extent=-phase, fill="#F0FFFF", outline="#2E3440")

def smooth_moon_animation(cancel_event):
    while True:
        if cancel_event.is_set():
            return
        update_moon_animation(remaining_time, total_time)
        time.sleep(1/60)

# Create the main window
root = tk.Tk()
root.title("Hibernate Timer")
root.geometry("350x350")
root.configure(bg="#2E3440")

# Set the window icon
root.iconbitmap("232.ico")

# Create and place the widgets
style = ttk.Style()
style.configure("Rounded.TEntry", relief="flat", borderwidth=1, foreground="#D8DEE9", background="#4C566A", padding=5)
style.map("Rounded.TEntry", fieldbackground=[("readonly", "#4C566A")])

tk.Label(root, text="Enter time in minutes:", bg="#2E3440", fg="#D8DEE9", font=("Lexend", 12, "bold")).pack(pady=10)
entry = ttk.Entry(root, font=("Lexend", 12, "bold"), style="Rounded.TEntry")
entry.pack(pady=5)

start_button = tk.Button(root, text="Start", command=start_hibernation, bg="#5E81AC", fg="#D8DEE9", font=("Lexend", 12, "bold"), relief="flat", overrelief="raised")
start_button.pack(pady=5)

cancel_button = tk.Button(root, text="Cancel", command=cancel_hibernation, state=tk.DISABLED, bg="#FF0000", fg="#FFFFFF", font=("Lexend", 12, "bold"), relief="flat", overrelief="raised")
cancel_button.pack(pady=5)

status_label = tk.Label(root, text="", bg="#2E3440", fg="#D8DEE9", font=("Lexend", 12, "bold"))
status_label.pack(pady=10)

# Create the canvas for the moon animation
canvas = tk.Canvas(root, width=100, height=100, bg="#2E3440", highlightthickness=0)
canvas.pack(pady=10)

# Run the application
root.mainloop()
