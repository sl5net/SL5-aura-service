# test_toplevel_umlaut.py
import threading
import tkinter as tk

_root = None
_ready = threading.Event()

def run_tk():
    global _root
    root = tk.Tk()
    root.withdraw()
    _root = root
    _ready.set()
    top = tk.Toplevel(root)
    text_area = tk.Text(top, width=40, height=5)
    text_area.pack()
    text_area.focus_set()
    root.mainloop()

t = threading.Thread(target=run_tk, daemon=True)
t.start()
_ready.wait()
t.join()
