import csv
from datetime import datetime

class WeatherDataAnalyzer:
    filename = 'leibnitz_weather_august_2024.csv'

    def __init__(self, file_path):
        self.file_path = file_path
        self.time_data = []
        self.temp_data = []
        self.humidity_data = []
        self.wind_speed_data = []

    def fetch_data(self):
        from meteostat import Point, Hourly
        from datetime import datetime

        leibnitz = Point(46.78, 15.54)

        start = datetime(2024, 8, 1)
        end = datetime(2024, 8, 31, 23, 59)

        data = Hourly(leibnitz, start, end)
        data = data.fetch()

        data_mod = data[['temp', 'rhum', 'wspd']]

        data_mod.to_csv(self.filename)

    def load_data(self):
        try:
            with open(self.file_path, mode='r') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)
                
                for row in csv_reader:
                    self.time_data.append(datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S'))
                    self.temp_data.append(float(row[1]))
                    self.humidity_data.append(float(row[2]))
                    self.wind_speed_data.append(float(row[3]))
            print("Daten erfolgreich geladen.")
        except FileNotFoundError:
            print("Fehler: Die Datei wurde nicht gefunden.")
        except ValueError as e:
            print(f"Fehler beim Verarbeiten der Daten: {e}")
        except Exception as e:
            print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

    def average_temperature(self):
        if not self.temp_data:
            print("Temperaturdaten fehlen.")
            return None
        avg_temp = sum(self.temp_data) / len(self.temp_data)
        print(f"Durchschnittliche Temperatur: {avg_temp:.2f} °C")
        return avg_temp

    def filter_humidity(self, min_humidity, max_humidity):
        filtered_data = [
            (self.time_data[i], self.temp_data[i], self.humidity_data[i], self.wind_speed_data[i])
            for i in range(len(self.humidity_data))
            if min_humidity <= self.humidity_data[i] <= max_humidity
        ]
        print(f"Daten gefiltert für Luftfeuchtigkeit zwischen {min_humidity}% und {max_humidity}%:")
        for data in filtered_data:
            print(data)
        return filtered_data

    def process_data(self, func):
        processed_temps = [func(temp) for temp in self.temp_data]
        print("Temperaturdaten nach Umrechnung:")
        for temp in processed_temps:
            print(f"{temp:.2f} °F")
        return processed_temps

    def min_max_temperature(self):
        if not self.temp_data:
            print("Temperaturdaten fehlen.")
            return None, None
        min_temp = min(self.temp_data)
        max_temp = max(self.temp_data)
        print(f"Niedrigste Temperatur: {min_temp:.2f} °C")
        print(f"Höchste Temperatur: {max_temp:.2f} °C")
        return min_temp, max_temp

analyzer = WeatherDataAnalyzer(WeatherDataAnalyzer.filename)

analyzer.fetch_data()
analyzer.load_data()
analyzer.average_temperature()
analyzer.filter_humidity(70, 80)
analyzer.process_data(lambda c: c * 9/5 + 32)
analyzer.min_max_temperature()
