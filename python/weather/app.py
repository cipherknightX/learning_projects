import datetime as dt
import requests
import urllib.parse
from flask import Flask, request, render_template

app = Flask(__name__)

BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
API_KEY = "cde1ded53fc75ea2d6248b7f582aefad"

def Kelvin_to_celsius_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius * (9/5) + 32
    return celsius, fahrenheit

@app.route('/', methods=['GET', 'POST'])
def index():
    city = None
    weather_info = None
    if request.method == 'POST':
        city = request.form['city']
        url = BASE_URL + urllib.parse.urlencode({"q": city, "appid": API_KEY, "units": "metric"})
        response = requests.get(url).json()

        temp_kelvin = response['main']['temp']
        temp_celsius, temp_fahrenheit = Kelvin_to_celsius_fahrenheit(temp_kelvin)
        feels_like_kelvin = response['main']['feels_like']
        feels_like_celsius, feels_like_fahrenheit = Kelvin_to_celsius_fahrenheit(feels_like_kelvin)
        wind_speed = response['wind']['speed']
        humidity = response['main']['humidity']
        description = response['weather'][0]['description']
        sunrise_time = dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
        sunset_time = dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])

        weather_info = {
            'city': city,
            'temp_celsius': temp_celsius,
            'temp_fahrenheit': temp_fahrenheit,
            'feels_like_celsius': feels_like_celsius,
            'feels_like_fahrenheit': feels_like_fahrenheit,
            'wind_speed': wind_speed,
            'humidity': humidity,
            'description': description,
            'sunrise_time': sunrise_time,
            'sunset_time': sunset_time
        }
    return render_template('index.html', weather_info=weather_info)

if __name__ == '__main__':
    app.run(debug=True)
