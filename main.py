import requests
import json
from datetime import datetime, timedelta
import os.path

CORD = [52.229676, 21.012229]
dates = {}


def user_date():
    print('Podaj interesującą Cię datę w formacie YYYY-MM-DD, ')
    date = input()
    try:
        date_format = datetime.strptime(date, "%Y-%m-%d")
        return date_format.date()

    except ValueError:
        print('Podano nieprawidłowy format daty. Program przyjmie dzień jutrzejszy.')
        return datetime.today() + timedelta(days=1)


def respo(CORD, formatdate):
    response = requests.get(
        f'https://api.open-meteo.com/v1/forecast?latitude={CORD[0]}&longitude={CORD[1]}&hourly=rain&daily=rain_sum&timezone=Europe%2FLondon&start_date={formatdate}&end_date={formatdate}')
    data = response.json()
    rain_sum = data["daily"]["rain_sum"]
    return rain_sum[0]


date = user_date()
formatdate = date.strftime("%Y-%m-%d")

if os.path.exists("weather.json"):
    with open("weather.json", "r") as f:
        dates = json.load (f)

if formatdate in dates:
    rain_sum = dates[formatdate]
else:
    dates[formatdate] = respo(CORD, formatdate)
    rain_sum = dates[formatdate]
    with open("weather.json", "w") as f:
        json.dump(dates, f)

if rain_sum > 0:
    print(f'Dnia {formatdate} będzie padać.')
elif rain_sum == 0:
    print(f'Dnia {formatdate} nie będzie padać.')
else:
    print(f'Nie wiemy czy dnia {formatdate} będzie padać.')
