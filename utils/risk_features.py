import pandas as pd


def build_risk_features(base_features, predicted_crowd):

    predicted_crowd_level = 0

    if predicted_crowd >= 20000:
        predicted_crowd_level = 2
    elif predicted_crowd >= 10000:
        predicted_crowd_level = 1

    predicted_temple_pressure = predicted_crowd / 1000

    predicted_crowd_weather_interaction = (
        predicted_crowd *
        base_features["weather_severity"].iloc[0]
    )

    predicted_weekend_crowd_interaction = (
        predicted_crowd
        if base_features["is_weekend"].iloc[0] == 1
        else 0
    )

    predicted_rain_crowd_interaction = (
        predicted_crowd *
        base_features["rain_intensity_num"].iloc[0]
    )

    predicted_final_risk_signal = (
        predicted_temple_pressure
        + base_features["weather_severity"].iloc[0]
    )

    risk_df = base_features.copy()

    risk_df["predicted_crowd"] = predicted_crowd
    risk_df["predicted_crowd_level"] = predicted_crowd_level

    risk_df["predicted_temple_pressure"] = predicted_temple_pressure

    risk_df["predicted_crowd_weather_interaction"] = (
        predicted_crowd_weather_interaction
    )

    risk_df["predicted_weekend_crowd_interaction"] = (
        predicted_weekend_crowd_interaction
    )

    risk_df["predicted_rain_crowd_interaction"] = (
        predicted_rain_crowd_interaction
    )

    risk_df["predicted_final_risk_signal"] = (
        predicted_final_risk_signal
    )

    return risk_df