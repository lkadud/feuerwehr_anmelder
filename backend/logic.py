import pandas as pd

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class BackendLogic:
    def __init__(self):
        self.driver = None#webdriver.Firefox()
        self.url = None
        self.teilnehmer = None
        self.anmelder = None

    def load_url(self, url, browser):
        if self.driver:
            self.driver.quit()
            self.driver=None
        if browser == "Firefox":
            self.driver = webdriver.Firefox()
        else:
            self.driver = webdriver.Chrome() #Check if chrome works as well...

        try:
            self.driver.get(url)
            self.url = url
            self.accept_cookie_banner()
        except selenium.common.exceptions.InvalidArgumentException as exception:
            return exception

    # Excel function
    def load_file_excel(self, filename):
        anmelder = pd.read_excel(filename, sheet_name="Anmelder", dtype=str)
        teilnehmer = pd.read_excel(filename, sheet_name="Teilnehmer", dtype=str)
        self.teilnehmer = teilnehmer
        self.anmelder = anmelder
        return anmelder, teilnehmer

    @staticmethod
    def convert_dataframe_to_table(df):
        coldata = list(df)
        rowdata = df.values.tolist()
        return coldata, rowdata

    def reset(self):
        if self.driver:
            self.driver.quit()
            self.driver=None
        
        if self.url:
            self.url = None

        if self.teilnehmer is not None:
            self.teilnehmer = None

        if self.anmelder is not None:
            self.anmelder = None


    # Webpage logic
    def accept_cookie_banner(self):
        try:
            # Locate the cookie acceptance button (replace with the actual identifier)
            cookie_accept_button = self.driver.find_element(By.ID, "cookiehinweis_store_options_accept_all")
            cookie_accept_button.click()
            print("Cookie banner accepted.")
        except Exception as e:
            print(f"Could not find the cookie banner: {e}")

    def accept_dataprivacy_checkboxes(self):
        try:
            self.insert_checkbox("dsh")
        except Exception as e:
            print(f"Could not find the data privacy checkbox: {e}")
        
        try:
            self.insert_checkbox("hwkf")
        except Exception as e:
            print(f"Could not find the hwkf checkbox: {e}")

        try:
            self.insert_checkbox("vollstaendigkf")
        except Exception as e:
            print(f"Could not find the data completenes checkbox: {e}")

    def accept_and_send_form(self):
        try:
            # Locate the cookie acceptance button (replace with the actual identifier)
            send_button = self.driver.find_element(By.XPATH, "//input[@class='fRight']")
            send_button.click()
            print("Cookie banner accepted.")
        except Exception as e:
            print(f"Could not find the cookie banner: {e}")

    def check(self):
        if self.driver is None:
            return False

    def process_anmelder(self):
        anmelder = self.anmelder.to_records()[0]
        self.insert_dropdown_searchable("rechnung_firma", anmelder.Feuerwehr)
        self.insert_dropdown("rechnung_anrede", anmelder.Anrede)
        self.insert_text("rechnung_vorname", anmelder.Vorname)
        self.insert_text("rechnung_nachname", anmelder.Nachname)
        self.insert_text("rechnung_anschrift", anmelder.Anschrift)
        self.insert_text("rechnung_plz", anmelder.PLZ)
        self.insert_dropdown_searchable("rechnung_ort", anmelder.Ort)
        self.insert_text("rechnung_telefon", anmelder.Telefon)
        self.insert_text("rechnung_email", anmelder.Email)
        self.insert_date("anmelder_geburtsdatum", anmelder.Geburtsdatum)

    def process_teilnehmers(self):
        teilnehmers = self.teilnehmer.to_records()
        i = len(teilnehmers)
        self.insert_dropdown("cnt", str(2)) # somehow get this number from page
        for id, teilnehmer in enumerate(teilnehmers, start=1):
            self.process_teilnehmer(id, teilnehmer)


    def process_teilnehmer(self, id, teilnehmer):
        self.insert_dropdown_searchable(f"tn_firma_{id}", teilnehmer.Feuerwehr)
        self.insert_dropdown(f"tn_funktion_{id}", teilnehmer.Funktion)
        self.insert_dropdown(f"tn_anrede_{id}", teilnehmer.Anrede)
        self.insert_text(f"tn_vname_{id}", teilnehmer.Vorname)
        self.insert_text(f"tn_nname_{id}", teilnehmer.Nachname)
        self.insert_text(f"tn_email_{id}", teilnehmer.Email)
        self.insert_date(f"tn_geburtsdatum_{id}", teilnehmer.Geburtsdatum)

    def insert_dropdown_searchable(self, key, value):
        dropdown_field = self.driver.find_element(By.ID, f"{key}_chosen")
        dropdown_field.click() 
        search_key = f"//div[@id='{key}_chosen']//input[@class='chosen-search-input']"
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, search_key)))
        dropdown_drop = self.driver.find_element(By.XPATH, search_key)
        dropdown_drop.send_keys(value)
        dropdown_drop.send_keys(Keys.RETURN)  

    def insert_dropdown(self, key, value):
        dropdown_field = self.driver.find_element(By.ID, key)
        dropdown = Select(dropdown_field)
        dropdown.select_by_visible_text(value)

    def insert_text(self, key, value):
        text_field = self.driver.find_element(By.ID, key)
        text_field.send_keys(value)

    def insert_date(self, key, value):
        date_field = self.driver.find_element(By.ID, key)
        date_field.clear()
        date_field.send_keys(value)

    def insert_checkbox(self, key):
        checkbox = self.driver.find_element(By.ID, key)
        self.driver.execute_script("arguments[0].click();", checkbox)
