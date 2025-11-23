import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

import tkinter as tk
#from tkinter import ttk
import ttkbootstrap as ttk
from frontend.app import ApplicationGUI


def main():
    def on_closing():
        if app.backend.driver:
            app.backend.driver.quit()
        root.destroy()

    root = ttk.Window(themename="journal")
    icon = tk.PhotoImage(file=resource_path("feuerwehrhelm.png"))
    root.iconphoto(True, icon)
    app = ApplicationGUI(root)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()


    # 1. Select URL
    # 2. Select Excel
    # 3. Misc settings (number of users?)
    # 4. Fill max number of users
    # 5. Repeat 4?