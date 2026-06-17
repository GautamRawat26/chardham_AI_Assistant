import pandas as pd
from datetime import datetime

SHRINE_MAP = {
    "Kedarnath": 0,
    "Badrinath": 1,
    "Gangotri": 2,
    "Yamunotri": 3
}

HISTORICAL_CROWD = {
    "Kedarnath": 10517,
    "Badrinath": 9379,
    "Gangotri": 4853,
    "Yamunotri": 4218
}


def build_features(
    shrine,
    weather,
    forecast_date=None
):

    if forecast_date:
        current_date = pd.to_datetime(
            forecast_date
        )
    else:
        current_date = datetime.now()

    temp = weather["temperature"]

    rain = (
        weather["precipitation_probability"]
        / 100
    )

    wind = weather["wind_speed"]

    humidity = weather["humidity"]

    day_of_week = current_date.weekday()

    is_weekend = (
        1 if day_of_week >= 5 else 0
    )

    month = current_date.month

    base_crowd = HISTORICAL_CROWD[shrine]

    lag_1 = base_crowd
    lag_3 = base_crowd
    lag_7 = base_crowd

    rolling_mean_7 = base_crowd

    trend = lag_1 - lag_3

    weather_cat_num = (
        1 if rain > 0 else 0
    )

    rain_intensity_num = 0

    if rain > 0.5:
        rain_intensity_num = 3

    elif rain > 0.2:
        rain_intensity_num = 2

    elif rain > 0:
        rain_intensity_num = 1

    weather_severity = (
        temp + (humidity / 10)
    )

    heavy_rain_flag = (
        1 if rain > 0.5 else 0
    )

    storm_flag = (
        1 if wind > 8 else 0
    )

    seasonal_factor = 1.1

    day_type_num = is_weekend

    shrine_num = SHRINE_MAP[shrine]

    darshan_duration = 60

    peak_hour_flag = 0

    features = {
        "temp": temp,
        "rain": rain,
        "wind": wind,
        "humidity": humidity,
        "weather_cat_num": weather_cat_num,
        "rain_intensity_num": rain_intensity_num,
        "weather_severity": weather_severity,
        "heavy_rain_flag": heavy_rain_flag,
        "storm_flag": storm_flag,
        "day_of_week": day_of_week,
        "is_weekend": is_weekend,
        "month": month,
        "seasonal_factor": seasonal_factor,
        "day_type_num": day_type_num,
        "shrine_num": shrine_num,
        "darshan_duration": darshan_duration,
        "peak_hour_flag": peak_hour_flag,
        "lag_1": lag_1,
        "lag_3": lag_3,
        "lag_7": lag_7,
        "rolling_mean_7": rolling_mean_7,
        "trend": trend
    }

    return pd.DataFrame([features])