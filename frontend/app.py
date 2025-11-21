import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
#from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview

from backend.logic import BackendLogic

class ApplicationGUI:
    def __init__(self, master):
        self.master = master
        self.backend = BackendLogic()
        
        master.title("Feuerwehr-Anmelder")
        master.geometry("1000x400")

        self.label = ttk.Label(master, text="Enter Data:")
        self.label.pack()
        
        self.entry = ttk.Entry(master)
        self.entry.pack()
        
        self.file_path = ""
        load_button = ttk.Button(master, text="Load Excel File", command=self.load_file_path)
        load_button.pack()

        self.process_button = ttk.Button(
            master, 
            text="Process", 
            command=self.on_process
        )
        self.process_button.pack()
        
        self.result_label = ttk.Label(master, text="")
        self.result_label.pack()

        import pandas as pd
        anmelder = pd.read_excel("./anmeldung.xlsx", sheet_name="Anmelder", dtype=str)
        teilnehmer = pd.read_excel("./anmeldung.xlsx", sheet_name="Teilnehmer", dtype=str)
        coldata = list(anmelder)
        rowdata= anmelder.values.tolist()

        dt = Tableview(
        master=master,
        coldata=coldata,
        rowdata=rowdata,
        paginated=False,
        searchable=False,
        autofit=True,
        disable_right_click=True,
        autoalign=False,
        height=2)
        dt.pack(fill=tk.BOTH, expand=tk.YES, padx=10, pady=10)

        coldata = list(teilnehmer)
        rowdata= teilnehmer.values.tolist()


        dt = Tableview(
        master=master,
        coldata=coldata,
        rowdata=rowdata,
        paginated=False,
        searchable=False,
        autofit=True,
        disable_right_click=True,
        autoalign=False,
        height=3)
        dt.pack(fill=tk.BOTH, expand=tk.YES, padx=10, pady=10)
    
    def load_file_path(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        import pandas as pd 
        print(pd.read_excel(self.file_path))

    def on_process(self):
        input_data = self.entry.get()
        if input_data:
            result = self.backend.process_data(input_data)
            self.result_label.config(text=result)
        else:
            messagebox.showwarning("Warning", "Please enter some data")