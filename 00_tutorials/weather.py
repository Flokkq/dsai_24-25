#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install meteostat')


# In[ ]:


from meteostat import Point, Hourly
import pandas as pd
from datetime import datetime

# Definiere den Standort für Leibnitz, Steiermark (Koordinaten: 46.78°N, 15.54°E)
leibnitz = Point(46.78, 15.54)

# Zeitraum definieren: August 2024
start = datetime(2024, 8, 1)
end = datetime(2024, 8, 31, 23, 59)

# Abrufen der stündlichen Wetterdaten für den definierten Zeitraum
data = Hourly(leibnitz, start, end)
data = data.fetch()

data_mod = data[['temp', 'rhum', 'wspd']]

# Speichern der Daten in eine CSV-Datei
data_mod.to_csv('leibnitz_weather_august_2024.csv')

print("Wetterdaten für August 2024 erfolgreich heruntergeladen und gespeichert in 'leibnitz_weather_august_2024.csv'")


# In[ ]:


data.head()


# In[ ]:


data_mod.head()


# In[ ]:


import matplotlib.pyplot as plt
import csv
from datetime import datetime

# Dateipfad zur CSV-Datei
file_path = '/mnt/data/leibnitz_weather_august_2024_filtered.csv'

# Listen zur Speicherung der Daten
time_data = []
temp_data = []
humidity_data = []
wind_speed_data = []

try:
    # Öffnen und Einlesen der CSV-Datei
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)  # Überspringen der Kopfzeile
        
        # Jede Zeile durchlaufen und die Werte zu den Listen hinzufügen
        for row in csv_reader:
            time_data.append(datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S'))
            temp_data.append(float(row[1]))
            humidity_data.append(float(row[2]))
            wind_speed_data.append(float(row[3]))
except FileNotFoundError:
    print("Fehler: Die Datei wurde nicht gefunden.")
except ValueError as e:
    print(f"Fehler beim Verarbeiten der Daten: {e}")
except Exception as e:
    print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

# Plotten der Daten
plt.figure(figsize=(14, 12))

# Temperaturdiagramm
plt.subplot(3, 1, 1)
plt.plot(time_data, temp_data, label='Temperatur (°C)', color='orange')
plt.title("Wetterdaten für August 2024 in Leibnitz")
plt.ylabel("Temperatur (°C)")
plt.legend()
plt.grid(True)

# Luftfeuchtigkeitsdiagramm
plt.subplot(3, 1, 2)
plt.plot(time_data, humidity_data, label='Luftfeuchtigkeit (%)', color='blue')
plt.ylabel("Luftfeuchtigkeit (%)")
plt.legend()
plt.grid(True)

# Windgeschwindigkeitsdiagramm
plt.subplot(3, 1, 3)
plt.plot(time_data, wind_speed_data, label='Windgeschwindigkeit (m/s)', color='green')
plt.ylabel("Windgeschwindigkeit (m/s)")
plt.xlabel("Datum")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
