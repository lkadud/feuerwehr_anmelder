import tkinter as tk
from tkinter import messagebox, filedialog
#from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
import ttkbootstrap.localization
ttkbootstrap.localization.initialize_localities = bool
from backend.logic import BackendLogic

class ApplicationGUI(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, padding=15, **kwargs)
        self.pack(fill=tk.BOTH, expand=tk.YES)
        #self.master = master
        
        self.backend = BackendLogic()
        
        master.title("Feuerwehr-Anmelder")
        master.geometry("1100x500")

        #menu = tk.Menu(master)
        #master.config(menu=menu)
        #menu.add_command(label="Reset", command=self.reset)

        self.frame = ttk.Labelframe(self, text="Einstellungen:", padding=15)
        self.frame.pack(fill=tk.X, expand=tk.YES)#grid(row=0, column=0, columnspan=3, sticky="ew")

        # URL-Input
        self.url = ""
        self.browser = tk.StringVar()
        self.frame_url = ttk.Frame(self.frame)
        self.frame_url.pack(fill=tk.X, expand=tk.YES)#grid(row=0, column=0, columnspan=3, sticky="ew")
        self.label_url = ttk.Label(self.frame_url, text="URL:", width=12)
        self.label_url.pack(side="left", padx=(15,0))
        self.entry_url = ttk.Entry(self.frame_url)
        self.entry_url.pack(side="left", fill=tk.X, expand=tk.YES, padx=5)#grid(row=0, column=1)
        self.dropdown_url = ttk.Combobox(self.frame_url, textvariable=self.browser, width=12)
        self.dropdown_url["values"] = ("Firefox", "Chrome")
        self.dropdown_url.current(0)
        self.dropdown_url["state"] = "readonly"
        self.dropdown_url.pack(side="left", padx=5)#.grid(row=0, column=2)
        self.button_url = ttk.Button(self.frame_url, text="Laden!", width=8, command=self.load_url)
        self.button_url.pack(side="left", padx=5)#grid(row=1, column=2, sticky='nsew')

        # Excel-Input
        self.file_path_excel = ""
        self.frame_excel = ttk.Frame(self.frame)
        self.frame_excel.pack(fill=tk.X, expand=tk.YES, pady=15)#.grid(row=1, column=0)
        self.label_excel = ttk.Label(self.frame_excel, text="Excel-Datei:", width=12)
        self.label_excel.pack(side="left", padx=(15,0))#.grid(row=3, column=0, sticky="w")
        self.entry_excel = ttk.Entry(self.frame_excel, text=self.file_path_excel)
        self.entry_excel.pack(side="left", fill=tk.X, expand=tk.YES, padx=5)#.grid(row=3, column=1)
        self.button_excel_search = ttk.Button(self.frame_excel, text="Durchsuchen...", bootstyle="secondary",width=12, command=self.search_file_path)
        self.button_excel_search.pack(side="left", padx=5)#.grid(row=3, column=2, sticky='nsew')
        self.button_excel_load = ttk.Button(self.frame_excel, text="Laden!", width=8, command=self.load_file_path)
        self.button_excel_load.pack(side="left", padx=5)#.grid(row=4, column=2, sticky='nsew')
        
        # Misc settings
        self.one_shot_var = tk.BooleanVar()
        self.frame_misc = ttk.Frame(self.frame)
        self.frame_misc.pack(fill=tk.X, expand=tk.YES, pady=15)#.grid(row=1, column=0)
        self.check_oneshot = ttk.Checkbutton(self.frame_misc, text="Oneshot", style="Squaretoggle.Toolbutton", variable=self.one_shot_var)
        self.check_oneshot.pack(side="right")
        
        # Start?
        self.sep = ttk.Separator(self.frame, orient=tk.HORIZONTAL)
        self.sep.pack(fill=tk.X, expand=tk.YES)
        self.frame_process = ttk.Frame(self.frame)
        self.frame_process.pack(fill=tk.X, expand=tk.YES, pady=15)#.grid(row=2, column=0)
        self.button_start = ttk.Button(self.frame_process, text="Start!", bootstyle="success", width=8, command=self.process)
        self.button_start.pack(side="right", padx=5)#grid(row=7, column=2, sticky="nsew")
        #self.button_start.pack()

        # Reset?
        self.button_reset = ttk.Button(self.frame_process, text="Reset!", bootstyle="secondary", width=8, command=self.reset)
        self.button_reset.pack(side="right", padx=5)#grid(row=7, column=0, sticky="nsew")

        self.table_frame = ttk.Frame(self)
        self.table_frame.pack(fill=tk.X, expand=tk.YES)#.grid(row=5, column=0, columnspan=3, sticky="nsew")
        self.dt = Tableview(
            master=self.table_frame,
            paginated=False,
            searchable=False,
            autofit=True,
            disable_right_click=True,
            autoalign=False,
            height=2
        )
        self.dt.pack(fill=tk.BOTH, expand=tk.YES, padx=10, pady=10)
        #self.dt.grid(row=5, columnspan=3, sticky="nsew")

        self.dt2 = Tableview(
            master=self.table_frame,
            paginated=False,
            searchable=False,
            autofit=True,
            disable_right_click=True,
            autoalign=False,
            height=3
        )
        #self.dt2.grid(row=6, columnspan=3, sticky="nsew")
        self.dt2.pack(fill=tk.BOTH, expand=tk.YES, padx=10, pady=10)

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
            self.backend.accept_dataprivacy_checkboxes()

            if self.check_oneshot.get():
                self.backend.accept_and_send_form()