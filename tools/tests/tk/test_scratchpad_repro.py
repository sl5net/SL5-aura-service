# tools/test/tk/test_scratchpad_repro.py
import queue
import threading
import tkinter as tk

_root = None
_ready = threading.Event()
_pending = queue.Queue()

def _poll(root):
    try:
        while True:
            cb = _pending.get_nowait()
            cb()
    except queue.Empty:
        pass
    root.after(30, lambda: _poll(root))

def run_tk():
    global _root
    root = tk.Tk()
    root.withdraw()
    _root = root
    _ready.set()
    root.after(30, lambda: _poll(root))
    root.mainloop()

def on_modified(event, text_area):
    text_area.edit_modified(False)
    print(f"modified, content={text_area.get('1.0', 'end-1c')!r}")

def build_window():
    top = tk.Toplevel(_root)
    text_area = tk.Text(top, width=40, height=5)
    text_area.pack()
    text_area.edit_modified(False)
    text_area.bind("<<Modified>>", lambda e: on_modified(e, text_area))
    top.lift()
    top.focus_force()
    text_area.focus_set()

t = threading.Thread(target=run_tk, daemon=True)
t.start()
_ready.wait()
_pending.put(build_window)
t.join()
