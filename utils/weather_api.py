import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TOMORROW_API_KEY")

SHRINE_COORDINATES = {
    "Kedarnath": {"lat": 30.7352, "lon": 79.0669},
    "Badrinath": {"lat": 30.7433, "lon": 79.4938},
    "Gangotri": {"lat": 30.9947, "lon": 78.9398},
    "Yamunotri": {"lat": 31.0140, "lon": 78.4600}
}


def get_shrine_coordinates(shrine):
    return SHRINE_COORDINATES.get(shrine)


def get_current_weather(shrine):
    coords = get_shrine_coordinates(shrine)

    lat = coords["lat"]
    lon = coords["lon"]

    url = "https://api.tomorrow.io/v4/weather/realtime"

    params = {
        "location": f"{lat},{lon}",
        "apikey": API_KEY
    }

    response = requests.get(url, params=params)
    return response.json()


def get_weather_forecast(shrine):
    coords = get_shrine_coordinates(shrine)

    lat = coords["lat"]
    lon = coords["lon"]

    url = "https://api.tomorrow.io/v4/weather/forecast"

    params = {
        "location": f"{lat},{lon}",
        "apikey": API_KEY
    }

    response = requests.get(url, params=params)
    forecast_json = response.json()
    print("RAW WEATHER RESPONSE:", forecast_json)
    return forecast_json


def extract_weather_data(weather_json):
    values = weather_json["data"]["values"]

    return {
        "temperature": values.get("temperature", 0),
        "humidity": values.get("humidity", 0),
        "wind_speed": values.get("windSpeed", 0),
        "visibility": values.get("visibility", 0),
        "precipitation_probability": values.get("precipitationProbability", 0),
        "weather_code": values.get("weatherCode", 0)
    }


def extract_daily_forecast(forecast_json, days):
    try:
        if not forecast_json:
            return []
        # safe navigation
        timelines = forecast_json.get("timelines")
        if not timelines:
            print("Missing timelines key:", forecast_json)
            return []
        daily_data = timelines.get("daily", [])
        if not daily_data:
            print("No daily data found:", forecast_json)
            return []
        return daily_data[:days]
    except Exception as e:
        print("Weather parsing error:", e)
        return []