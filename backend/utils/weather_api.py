# Weather API logic
import os
import requests

def get_current_weather(location):
    api_key = os.getenv('WEATHER_API_KEY')
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
