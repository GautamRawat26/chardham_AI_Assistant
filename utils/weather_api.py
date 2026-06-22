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
    return response.json()


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


def extract_daily_forecast(forecast_json, days=7):
    forecast_days = []

    if "timelines" in forecast_json:
        daily_data = forecast_json["timelines"].get("daily", [])
    else:
        daily_data = []
        print("Invalid API response:", forecast_json)

    for day in daily_data[:days]:
        values = day["values"]

        forecast_days.append({
            "date": day["time"][:10],
            "temperature": values.get("temperatureAvg", 0),
            "humidity": values.get("humidityAvg", 0),
            "wind_speed": values.get("windSpeedAvg", 0),
            "precipitation_probability": values.get("precipitationProbabilityAvg", 0),
            "weather_code": values.get("weatherCodeMax", 0),
            "visibility": values.get("visibilityAvg", 10)
        })

    return forecast_days