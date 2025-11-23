import tkinter as tk
from tkinter import messagebox, filedialog
#from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview

from backend.logic import BackendLogic

class ApplicationGUI:
    def __init__(self, master):
        self.master = master
        self.backend = BackendLogic()
        
        master.title("Feuerwehr-Anmelder")
        #master.geometry("680x420")

        #menu = tk.Menu(master)
        #master.config(menu=menu)
        #menu.add_command(label="Reset", command=self.reset)

        # URL-Input
        self.url = ""
        self.browser = tk.StringVar()
        self.label_url = ttk.Label(master, text="URL:", justify="left")
        self.label_url.grid(row=0, column=0, sticky="w")
        self.entry_url = ttk.Entry(master)
        self.entry_url.grid(row=0, column=1)
        self.button_url = ttk.Button(master, text="Laden!", command=self.load_url)
        self.button_url.grid(row=1, column=2, sticky='nsew')
        self.dropdown_url = ttk.Combobox(master, textvariable=self.browser)
        self.dropdown_url["values"] = ("Firefox", "Chrome")
        self.dropdown_url.current(0)
        self.dropdown_url["state"] = "readonly"
        self.dropdown_url.grid(row=0, column=2)
        tk.Label(master).grid(column=2) #Placeholder?

        # Excel-Input
        self.file_path_excel = ""
        self.label_excel = ttk.Label(master, text="Excel-Datei:", justify="left")
        self.label_excel.grid(row=3, column=0, sticky="w")
        self.entry_excel = ttk.Entry(master, text=self.file_path_excel)
        self.entry_excel.grid(row=3, column=1)
        self.button_excel_search = ttk.Button(master, text="Durchsuchen...", bootstyle="secondary", command=self.search_file_path)
        self.button_excel_search.grid(row=3, column=2, sticky='nsew')
        self.button_excel_load = ttk.Button(master, text="Laden!", command=self.load_file_path)
        self.button_excel_load.grid(row=4, column=2, sticky='nsew')
        
        
        # Start?
        self.button_start = ttk.Button(self.master, text="Start!", bootstyle="success", command=self.process)
        self.button_start.grid(row=7, column=2, sticky="nsew")
        #self.button_start.pack()

        # Reset?
        self.button_reset = ttk.Button(self.master, text="Reset!", bootstyle="secondary", command=self.reset)
        self.button_reset.grid(row=7, column=0, sticky="nsew")

        self.dt = Tableview(
            master=master,
            paginated=False,
            searchable=False,
            autofit=True,
            disable_right_click=True,
            autoalign=False,
            height=2
        )
        #dt.pack(fill=tk.BOTH, expand=tk.YES, padx=10, pady=10)
        self.dt.grid(row=5, columnspan=3, sticky="nsew")

        self.dt2 = Tableview(
            master=master,
            paginated=False,
            searchable=False,
            autofit=True,
            disable_right_click=True,
            autoalign=False,
            height=3
        )
        self.dt2.grid(row=6, columnspan=3, sticky="nsew")
        #dt.pack(fill=tk.BOTH, expand=tk.YES, padx=10, pady=10)

    def load_url(self):
        self.url = self.entry_url.get()
        if self.url:
            if self.backend.load_url(self.url, self.browser.get()):
                messagebox.showwarning("Warnung", "Bitte URL überprüfen!")
        else:
            messagebox.showwarning("Warnung", "Keine URL!")
    
    def load_file_path(self): #try excepts?
        self.file_path = self.entry_excel.get()
        if self.file_path:
            self.anmelder, self.teilnehmer = self.backend.load_file_excel(self.file_path)
            self.dt.build_table_data(*self.backend.convert_dataframe_to_table(self.anmelder))
            self.dt.reset_table()
            self.dt2.build_table_data(*self.backend.convert_dataframe_to_table(self.teilnehmer))
            self.dt2.reset_table()

        else:
            messagebox.showwarning("Warnung", "Kein Dateiname!")
        
    def search_file_path(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        self.entry_excel.insert(10, self.file_path)

    def reset(self):
        self.dt.purge_table_data()
        self.dt2.purge_table_data()
        self.entry_excel.delete(0, "end")
        self.entry_url.delete(0, "end")

        self.backend.reset()

    def process(self):
        if self.backend.check():
            self.backend.process_anmelder()
            self.backend.process_teilnehmers()