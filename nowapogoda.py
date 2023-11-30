import requests
import json
from datetime import datetime, timedelta
import os.path

location = [52.229676, 21.012229]


class WeatherForecast:
    dates = {}

    def __init__(self, date=''):
        self.date = date
        if os.path.exists("weather.json"):
            with open("weather.json", "r") as f:
                self.dates = json.load(f)
            print('Daty zapisane w programie:')
            for date in self:
                print(date)

    def __iter__(self):
        if len(self.dates) > 0:
            return iter(self.dates.keys())

    def __getitem__(self, date):
        try:
            datetime.strptime(date, "%Y-%m-%d")
            print(f'Sprawdzam pogodę dla {date}')
        except ValueError:
            print("Podano nieprawidłowy format daty. Program przyjmie dzień jutrzejszy.")
            date = datetime.today() + timedelta(days=1)
            date = date.strftime("%Y-%m-%d")
            print(f'Sprawdzam pogodę dla {date}')

        if date in self.dates:
            rain_sum = self.dates[date]
        else:
            response = requests.get(
                f'https://api.open-meteo.com/v1/forecast?latitude={location[0]}&longitude={location[1]}&hourly=rain&daily=rain_sum&timezone=Europe%2FLondon&start_date={date}&end_date={date}')
            data = response.json()
            rain_sum = data["daily"]["rain_sum"]
            self.dates[date] = rain_sum[0]
            rain_sum = rain_sum[0]
            with open("weather.json", "w") as f:
                json.dump(self.dates, f)
        if rain_sum > 0:
            print('Będzie padać.')
        elif rain_sum == 0:
            print('Nie będzie padać.')
        else:
            print('Nie wiemy.')

    def __setitem__(self, date, rain_sum):
        if isinstance(rain_sum, (int, float)):
            self.dates[date] = rain_sum
            with open("weather.json", "w") as f:
                json.dump(self.dates, f)

    def items(self):
        for key, value in self.dates.items():
            yield key, value


user_date = input('Podaj datę dla szukanej pogody: ')

weather_forecast = WeatherForecast()
weather_forecast[user_date]

for item in weather_forecast.items():
    print(item)
