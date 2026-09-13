# scratchpad_process.py
from multiprocessing import Process
import tkinter as tk

def run_scratchpad():
    root = tk.Tk()
    # baue UI auf
    root.mainloop()

def spawn():
    p = Process(target=run_scratchpad, daemon=True)
    p.start()
    return p

if __name__ == "__main__":
    spawn()
