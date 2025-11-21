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
    root = ttk.Window(themename="journal")
    #menu = tk.Menu(root)
    #root.config(menu=menu)
    #menu.add_command(label="Exit", command=quit)
    
    icon = tk.PhotoImage(file=resource_path("feuerwehrhelm.png"))
    root.iconphoto(True, icon)
    app = ApplicationGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()


    # 1. Select URL
    # 2. Select Excel
    # 3. Misc settings (number of users?)
    # 4. Fill max number of users
    # 5. Repeat 4?