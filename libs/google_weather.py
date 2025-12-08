import requests
import json
import googlemaps
import logging
import os

from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
api_key = os.getenv('google_api')
gmaps = googlemaps.Client(key=api_key)

def get_latlng(location):
    geocode_result = gmaps.geocode(location)
    return geocode_result[0]['geometry']['location']

def get_current_weather():
    location = os.getenv('location')
    latlng = get_latlng(location)
    URL = 'https://weather.googleapis.com/v1/currentConditions:lookup'
    params = {
        "key": api_key,
        "location.latitude": latlng['lat'],
        "location.longitude": latlng['lng']
    }
    response = requests.get(URL, params=params)
    weather = json.loads(response.text)
    return weather

def get_weather_condition_icon(icon_uri, condition):
    if not Path('/icons/' + str(condition) + '.png').exists():
        logging.info(f'Downloading icon for condition: {condition}')

        img_data = requests.get(icon_uri).content
        with open('/icons/' + str(condition) + '.png', 'wb') as handler:
            handler.write(img_data)
    else:
        logging.info(f'Icon for condition: {condition} already exists. Using cached version.')
    
    return '/icons/' + str(condition) + '.png'

def get_current_weather_display_info():
    current = get_current_weather()
    weather = {}
    icon_uri = current["weatherCondition"]["iconBaseUri"] + ".png"
    
    weather["temperature"] = current["temperature"]["degrees"]
    weather["condition"] = current["weatherCondition"]["description"]["text"]
    weather["condition_icon"] = get_weather_condition_icon(icon_uri, weather["condition"])

    return weather
