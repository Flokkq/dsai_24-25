import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def is_ready(browser):
    return browser.execute_script("return document.readyState === 'complete'")

options = webdriver.ChromeOptions()
# options.add_argument("headless")
browser = webdriver.Chrome(options=options)

results = []

try:
    browser.get("https://www.autoscout24.at/")
    WebDriverWait(browser, 20).until(is_ready)

    try:
        cookie_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='as24-cmp-accept-all-button']"))
        )
        cookie_button.click()
        time.sleep(1)
    except Exception as e:
        print("Cookie-Banner nicht gefunden oder bereits geschlossen.", e)

    # Marke auswählen (BMW)
    make_select = Select(WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "make"))
    ))
    make_select.select_by_visible_text("BMW")
    # Warten, bis das Modell-Dropdown aktualisiert
    # Sonst gibt es einen StaleElementReferenceError
    time.sleep(1)  

    # Modell auswählen (114)
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, "model")))
    model_select = Select(browser.find_element(By.ID, "model"))
    model_select.select_by_value("20149")  # Option "114" hat hier den Value "20149"

    # Maximalpreis auswählen (15.000)
    price_select = Select(WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "price"))
    ))
    price_select.select_by_visible_text("€ 15 000")

    search_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, "search-mask-search-cta"))
    )
    search_button.click()

    WebDriverWait(browser, 30).until(is_ready)
    time.sleep(2)

    def extract_results():
        page_results = []
        items = browser.find_elements(By.CSS_SELECTOR, "div.ListItem_wrapper__TxHWu")
        print("Gefundene Einträge auf der Seite:", len(items))
        for item in items:
            try:
                # Fahrzeugbezeichnung
                title_elem = item.find_element(By.CSS_SELECTOR, "a.ListItem_title__ndA4s h2")
                fahrzeugbezeichnung = title_elem.text.strip()

                # Preis
                preis_elem = item.find_element(By.CSS_SELECTOR, "p[data-testid='regular-price']")
                preis = preis_elem.text.strip()

                # Kilometerstand
                km_elem = item.find_element(By.CSS_SELECTOR, "span[data-testid='VehicleDetails-mileage_road']")
                kilometerstand = km_elem.text.strip()

                # Erstzulassung 
                erstzulassung_elem = item.find_element(By.CSS_SELECTOR, "span[data-testid='VehicleDetails-calendar']")
                erstzulassung = erstzulassung_elem.text.strip()
                baujahr = erstzulassung.split('/')[-1] if '/' in erstzulassung else erstzulassung

                # Leistung (kW/PS)
                leistung_elem = item.find_element(By.CSS_SELECTOR, "span[data-testid='VehicleDetails-speedometer']")
                leistung = leistung_elem.text.strip()

                try:
                    img_elem = item.find_element(By.CSS_SELECTOR, "img[data-testid='list-gallery-image']")
                    bild_url = img_elem.get_attribute("src")
                except Exception:
                    bild_url = None

                page_results.append({
                    "Fahrzeugbezeichnung": fahrzeugbezeichnung,
                    "Preis": preis,
                    "Kilometerstand": kilometerstand,
                    "Baujahr": baujahr,
                    "Leistung": leistung,
                    "Bild": bild_url
                })
            except Exception as e:
                print("Fehler beim Extrahieren eines Eintrags:", e)
        return page_results

    results.extend(extract_results())

    for r in results:
        print(r)

finally:
    browser.quit()


import pandas as pd
import matplotlib.pyplot as plt
import re
from datetime import datetime

df = pd.DataFrame(results)

current_year = datetime.now().year
df['Baujahr'] = pd.to_numeric(df['Baujahr'], errors='coerce')
df['Alter'] = current_year - df['Baujahr']

df['Kilometerstand'] = df['Kilometerstand'].str.replace(' km', '').str.replace(' ', '')
df['Kilometerstand'] = pd.to_numeric(df['Kilometerstand'], errors='coerce')

def extract_kw(text):
    match = re.search(r"(\d+)\s*kW", text)
    return float(match.group(1)) if match else None

df['kW'] = df['Leistung'].apply(extract_kw)

# Diagramm 1: Histogramm der Altersverteilung
plt.figure(figsize=(10,6))
plt.hist(df['Alter'].dropna(), bins=range(int(df['Alter'].min()), int(df['Alter'].max())+2), edgecolor='black')
plt.title("Altersverteilung der Fahrzeuge")
plt.xlabel("Alter (Jahre)")
plt.ylabel("Anzahl Fahrzeuge")
plt.show()

# Diagramm 2: Bubble Chart (Alter vs. Kilometerstand, Bubble Size = kW)
plt.figure(figsize=(10,6))
bubble_sizes = df['kW'].fillna(0) * 10  
plt.scatter(df['Alter'], df['Kilometerstand'], s=bubble_sizes, alpha=0.5)
plt.title("Fahrzeugdaten: Alter, Kilometerstand und Leistung")
plt.xlabel("Alter (Jahre)")
plt.ylabel("Kilometerstand")
plt.show()
