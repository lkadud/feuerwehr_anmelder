import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

if __name__ == "__main__":
    anmelder = pd.read_excel("./anmeldung.xlsx", sheet_name="Anmelder", dtype=str)
    teilnehmer = pd.read_excel("./anmeldung.xlsx", sheet_name="Teilnehmer", dtype=str)
    anmelder = anmelder.to_records()[0]
    teilnehmer = teilnehmer.to_records()
    print(anmelder)
    print(teilnehmer)
    
    # Set up the WebDriver (using Chrome in this example)
    driver = webdriver.Firefox()
    driver.get("<add-url>")
    time.sleep(2)

    # Accepting cookies
    try:
        # Locate the cookie acceptance button (replace with the actual identifier)
        cookie_accept_button = driver.find_element(By.ID, "cookiehinweis_store_options_accept_all")
        cookie_accept_button.click()
        print("Cookie banner accepted.")
    except Exception as e:
        print(f"Could not find the cookie banner: {e}")
    time.sleep(5)
    

    checkbox = driver.find_element(By.ID, "dsh")
    driver.execute_script("arguments[0].click();", checkbox)

    checkbox = driver.find_element(By.ID, "hwkf")
    driver.execute_script("arguments[0].click();", checkbox)

    checkbox = driver.find_element(By.ID, "vollstaendigkf")
    driver.execute_script("arguments[0].click();", checkbox)
    #print(checkbox.get_attribute("data-err"))
    #checkbox.click()


    #submit_button = driver.find_element(By.XPATH, "//input[@class='fRight']")
    #submit_button.click()

    """
    try:
        # Anmelder
        feuerwehr_field = driver.find_element(By.ID, "rechnung_firma_chosen")
        feuerwehr_field.click()     
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='rechnung_firma_chosen']//input[@class='chosen-search-input']")))
        feuerwehr_drop = driver.find_element(By.XPATH, "//div[@id='rechnung_firma_chosen']//input[@class='chosen-search-input']")
        feuerwehr_drop.send_keys(anmelder.Feuerwehr)
        feuerwehr_drop.send_keys(Keys.RETURN)        
        
        anrede_field = driver.find_element(By.ID, "rechnung_anrede")
        anrede = Select(anrede_field)
        anrede.select_by_visible_text(anmelder.Anrede)

        vorname_field = driver.find_element(By.ID, "rechnung_vorname")
        vorname_field.send_keys(anmelder.Vorname)

        name_field = driver.find_element(By.ID, "rechnung_nachname")
        name_field.send_keys(anmelder.Nachname)

        anschrift_field = driver.find_element(By.ID, "rechnung_anschrift")
        anschrift_field.send_keys(anmelder.Anschrift)

        plz_field = driver.find_element(By.ID, "rechnung_plz")
        plz_field.send_keys(anmelder.PLZ)

        ort_field = driver.find_element(By.ID, "rechnung_ort_chosen")
        ort_field.click()     
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='rechnung_ort_chosen']//input[@class='chosen-search-input']")))
        ort_drop = driver.find_element(By.XPATH, "//div[@id='rechnung_ort_chosen']//input[@class='chosen-search-input']")
        ort_drop.send_keys(anmelder.Ort)
        ort_drop.send_keys(Keys.RETURN)

        telefon_field = driver.find_element(By.ID, "rechnung_telefon")
        telefon_field.send_keys(anmelder.Telefon)

        mail_field = driver.find_element(By.ID, "rechnung_email")
        mail_field.send_keys(anmelder.Email)

        geburt_field = driver.find_element(By.ID, "anmelder_geburtsdatum")
        geburt_field.clear()
        geburt_field.send_keys(anmelder.Geburtsdatum)

        #Teilnehmer
        number_of_tns = 1
        for i in range(1,teilnehmer.shape[0]+1):
            feuerwehr_field = driver.find_element(By.ID, f"tn_firma_{i}_chosen")
            feuerwehr_field.click()     
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//div[@id='tn_firma_{i}_chosen']//input[@class='chosen-search-input']")))
            feuerwehr_drop = driver.find_element(By.XPATH, f"//div[@id='tn_firma_{i}_chosen']//input[@class='chosen-search-input']")
            feuerwehr_drop.send_keys(teilnehmer[i].Feuerwehr)
            feuerwehr_drop.send_keys(Keys.RETURN)      

            funktion_field = driver.find_element(By.ID, f"tn_funktion_{i}")
            funktion = Select(funktion_field)
            funktion.select_by_visible_text(teilnehmer[i].Funktion)

            anrede_field = driver.find_element(By.ID, f"tn_anrede_{i}")
            anrede = Select(anrede_field)
            anrede.select_by_visible_text(teilnehmer[i].Anrede)

            vorname_field = driver.find_element(By.ID, f"tn_vname_{i}")
            vorname_field.send_keys(teilnehmer[i].Vorname)

            name_field = driver.find_element(By.ID, f"tn_nname_{i}")
            name_field.send_keys(teilnehmer[i].Nachname)

            mail_field = driver.find_element(By.ID, f"tn_email_{i}")
            mail_field.send_keys(teilnehmer[i].Email)

            geburt_field = driver.find_element(By.ID, f"tn_geburtsdatum_{i}")
            geburt_field.clear()
            geburt_field.send_keys(teilnehmer[i].Geburtsdatum)

            time.sleep(10000)
    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(1000)
    """
    time.sleep(10000)
    driver.quit()