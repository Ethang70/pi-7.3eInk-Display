import requests
import json
import googlemaps
from datetime import datetime
import os
from dotenv import load_dotenv

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