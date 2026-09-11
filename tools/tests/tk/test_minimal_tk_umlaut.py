# tools/test/test_minimal_tk_umlaut.py
import tkinter as tk

def on_key(event):
    print(f"key={event.keysym!r} char={event.char!r}")

root = tk.Tk()
text_area = tk.Text(root, width=40, height=5)
text_area.pack()
text_area.bind("<KeyPress>", on_key)
text_area.focus_set()
root.mainloop()
