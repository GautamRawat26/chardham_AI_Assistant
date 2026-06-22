import streamlit as st
import joblib
import pandas as pd
import plotly.graph_objects as go

from utils.weather_api import (
    get_weather_forecast,
    extract_daily_forecast
)

from utils.feature_engineering import build_features
from utils.risk_features import build_risk_features

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Smart AI Chardham Assistant",
    page_icon="🛕",
    layout="wide"
)

st.title("🛕 Smart AI Chardham Assistant")
st.markdown("### AI-Based Crowd & Risk Prediction System")

# ==================================================
# CONSTANTS
# ==================================================

RISK_COLORS = {
    "Safe": ("🟢", "#d4edda", "#155724"),
    "Moderate": ("🟡", "#fff3cd", "#856404"),
    "High": ("🔴", "#f8d7da", "#721c24"),
}

# Final real-world recommendation logic
# Lower score = better travel day
SCORE_WEIGHTS = {
    "High Risk Probability": 0.40,
    "Rain": 0.25,
    "Weather Severity": 0.15,
    "Wind": 0.10,
    "Crowd": 0.07,
    "Humidity": 0.03,
}

# ==================================================
# HELPERS
# ==================================================

def normalize_series(series: pd.Series) -> pd.Series:
    if series.max() == series.min():
        return pd.Series(0.0, index=series.index)
    return (series - series.min()) / (series.max() - series.min())


def build_recommendation_df(forecast_df: pd.DataFrame) -> pd.DataFrame:
    df = forecast_df.copy()

    # Derived feature for recommendation only
    # Higher value = worse weather conditions
    df["Weather Severity"] = df["Temperature"] + (df["Humidity"] / 10)

    df["Risk_N"] = normalize_series(df["High Risk Probability"])
    df["Rain_N"] = normalize_series(df["Rain"])
    df["Severity_N"] = normalize_series(df["Weather Severity"])
    df["Wind_N"] = normalize_series(df["Wind"])
    df["Crowd_N"] = normalize_series(df["Crowd"])
    df["Humidity_N"] = normalize_series(df["Humidity"])

    # Weighted recommendation score
    df["Recommendation Score"] = (
        SCORE_WEIGHTS["High Risk Probability"] * df["Risk_N"] +
        SCORE_WEIGHTS["Rain"] * df["Rain_N"] +
        SCORE_WEIGHTS["Weather Severity"] * df["Severity_N"] +
        SCORE_WEIGHTS["Wind"] * df["Wind_N"] +
        SCORE_WEIGHTS["Crowd"] * df["Crowd_N"] +
        SCORE_WEIGHTS["Humidity"] * df["Humidity_N"]
    )

    ranking_df = df.sort_values(
        by="Recommendation Score",
        ascending=True
    ).reset_index(drop=True)

    ranking_df["Rank"] = ranking_df.index + 1

    reasons = []
    for _, row in ranking_df.iterrows():
        reason_parts = []

        if row["High Risk Probability"] == df["High Risk Probability"].min():
            reason_parts.append("Lowest risk probability")

        if row["Rain"] == df["Rain"].min():
            reason_parts.append("Lowest rain probability")

        if row["Weather Severity"] == df["Weather Severity"].min():
            reason_parts.append("Most comfortable weather")

        if row["Wind"] == df["Wind"].min():
            reason_parts.append("Calmest wind")

        if row["Crowd"] == df["Crowd"].min():
            reason_parts.append("Lowest crowd")

        if row["Humidity"] <= df["Humidity"].median():
            reason_parts.append("Comfortable humidity")

        if not reason_parts:
            reason_parts.append("Balanced overall conditions")

        reasons.append(", ".join(reason_parts))

    ranking_df["Why Recommended"] = reasons

    return ranking_df


def show_forecast_table(forecast_df: pd.DataFrame):
    st.subheader("📅 Forecast Results")

    st.dataframe(
        forecast_df[
            [
                "Date",
                "Temperature",
                "Humidity",
                "Wind",
                "Rain",
                "Visibility",
                "Crowd",
                "Risk",
                "High Risk Probability"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


def show_best_day_recommendation(forecast_df: pd.DataFrame, ranking_df: pd.DataFrame):
    best = ranking_df.iloc[0]
    risk_icon, bg_color, text_color = RISK_COLORS.get(
        best["Risk"],
        ("⚪", "#f8f9fa", "#343a40")
    )

    st.markdown("---")
    st.subheader("🏆 AI Travel Recommendation")

    st.markdown(
        f"""
        <div style="
            background:{bg_color};
            color:{text_color};
            border-radius:12px;
            padding:18px 24px;
            margin-bottom:16px;
        ">
            <h3 style="margin:0;color:{text_color};">📅 Recommended: {best['Date']}</h3>
            <p style="margin:6px 0 0 0;font-size:15px;">
                {risk_icon} Risk: <strong>{best['Risk']}</strong> &nbsp;|&nbsp;
                👥 Expected Crowd: <strong>{int(best['Crowd']):,}</strong> &nbsp;|&nbsp;
                🌧 Rain: <strong>{best['Rain']}%</strong> &nbsp;|&nbsp;
                🔴 High Risk Prob.: <strong>{best['High Risk Probability']:.1f}%</strong>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("#### 🔍 Why This Day?")

    reasons = []

    if best["High Risk Probability"] == forecast_df["High Risk Probability"].min():
        reasons.append(f"⚠ Lowest high-risk probability at {best['High Risk Probability']:.1f}%.")

    if best["Rain"] == forecast_df["Rain"].min():
        reasons.append(f"☔ Lowest rain probability ({best['Rain']}%) among all forecast days.")
    elif best["Rain"] < 30:
        reasons.append(f"☔ Rain probability is low at {best['Rain']}%.")

    if best["Weather Severity"] == (forecast_df["Temperature"] + (forecast_df["Humidity"] / 10)).min():
        reasons.append("🌡 Most comfortable overall weather severity.")

    if best["Crowd"] == forecast_df["Crowd"].min():
        reasons.append(f"👥 Least crowded day — only {int(best['Crowd']):,} pilgrims expected.")
    else:
        reasons.append(f"👥 Manageable crowd of {int(best['Crowd']):,} expected.")

    if best["Wind"] <= 5:
        reasons.append(f"💨 Calm winds at {best['Wind']} m/s — safe for travel.")
    elif best["Wind"] < 8:
        reasons.append(f"💨 Moderate winds ({best['Wind']} m/s) — generally acceptable.")

    if 8 <= best["Temperature"] <= 20:
        reasons.append(f"🌡 Comfortable temperature of {best['Temperature']} °C.")
    elif best["Temperature"] > 5:
        reasons.append(f"🌡 Temperature ({best['Temperature']} °C) is manageable.")

    if best["Humidity"] <= forecast_df["Humidity"].median():
        reasons.append(f"💧 Comfortable humidity ({best['Humidity']}%).")

    if best["Visibility"] >= 8:
        reasons.append(f"👁 Good visibility of {best['Visibility']} km.")

    for reason in reasons:
        st.markdown(f"- {reason}")

    st.markdown(
        "\n> 🧭 This recommendation is generated by comparing all forecast days using "
        "high-risk probability, rain, weather severity, wind, crowd, and humidity."
    )


def show_ranking_table(ranking_df: pd.DataFrame):
    st.markdown("---")
    st.subheader("🥇 Travel Ranking")

    st.dataframe(
        ranking_df[
            [
                "Rank",
                "Date",
                "Crowd",
                "Rain",
                "Wind",
                "Temperature",
                "Risk",
                "High Risk Probability",
                "Why Recommended"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


def show_crowd_chart(forecast_df: pd.DataFrame, best_date):
    st.markdown("---")
    st.subheader("📈 Crowd Forecast Chart")

    df = forecast_df.copy()
    df["IsBest"] = df["Date"] == best_date

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["Date"],
        y=df["Crowd"],
        mode="lines+markers",
        name="Predicted Crowd",
        line=dict(width=2.5, color="#1f77b4"),
        marker=dict(
            size=[14 if x else 8 for x in df["IsBest"]],
            color=["#28a745" if x else "#1f77b4" for x in df["IsBest"]],
            line=dict(width=2, color="white"),
        ),
        hovertemplate="<b>%{x}</b><br>Crowd: %{y:,}<extra></extra>",
    ))

    best_row = df[df["IsBest"]]
    if not best_row.empty:
        fig.add_annotation(
            x=best_row["Date"].values[0],
            y=best_row["Crowd"].values[0],
            text="🏆 Best Day",
            showarrow=True,
            arrowhead=2,
            arrowcolor="#28a745",
            font=dict(color="#28a745", size=12),
            yshift=20,
        )

    fig.update_layout(
        title="Predicted Crowd Across Forecast Days",
        xaxis_title="Date",
        yaxis_title="Predicted Crowd",
        hovermode="x unified",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        "Green marker = recommended travel day. Lower crowd levels mean a more comfortable pilgrimage experience."
    )


def show_weather_comparison_chart(forecast_df: pd.DataFrame):
    st.markdown("---")
    st.subheader("🌡 Weather Feature Comparison")

    fig = go.Figure()

    feature_cfg = [
        ("Temperature", "🌡 Temperature (°C)"),
        ("Humidity", "💧 Humidity (%)"),
        ("Rain", "🌧 Rain Prob. (%)"),
        ("Wind", "💨 Wind (m/s)"),
    ]

    for col, label in feature_cfg:
        if col in forecast_df.columns:
            fig.add_trace(go.Scatter(
                x=forecast_df["Date"],
                y=forecast_df[col],
                mode="lines+markers",
                name=label,
                line=dict(width=2),
                marker=dict(size=7),
                hovertemplate=f"<b>%{{x}}</b><br>{label}: %{{y}}<extra></extra>",
            ))

    fig.update_layout(
        title="Key Weather Metrics Over Forecast Period",
        xaxis_title="Date",
        yaxis_title="Value",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig, use_container_width=True)


def show_complete_weather_section(forecast_df: pd.DataFrame):
    ranking_df = build_recommendation_df(forecast_df)

    show_forecast_table(forecast_df)
    show_best_day_recommendation(forecast_df, ranking_df)
    show_ranking_table(ranking_df)
    show_crowd_chart(forecast_df, ranking_df.iloc[0]["Date"])
    show_weather_comparison_chart(forecast_df)

# ==================================================
# LOAD MODELS
# ==================================================

try:
    crowd_model = joblib.load("models/crowd_xgb_model.pkl")
    risk_model = joblib.load("models/risk_rf_model.pkl")
    st.success("✅ Models Loaded Successfully")
except Exception as e:
    st.exception(e)
    st.stop()

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.header("📍 Travel Inputs")

shrine = st.sidebar.selectbox(
    "Select Shrine",
    [
        "Kedarnath",
        "Badrinath",
        "Gangotri",
        "Yamunotri"
    ]
)

days = st.sidebar.slider(
    "Forecast Days",
    1,
    7,
    3
)

# ==================================================
# PREDICT
# ==================================================

if st.button("🚀 Generate Prediction", use_container_width=True):

    try:
        forecast_json = get_weather_forecast(shrine)
        st.write(forecast_json)

        forecast_days = extract_daily_forecast(
            forecast_json,
            days
        )

        results = []

        for day_weather in forecast_days:

            X = build_features(
                shrine=shrine,
                weather=day_weather,
                forecast_date=day_weather["date"]
            )

            predicted_crowd = float(
                crowd_model.predict(X)[0]
            )

            risk_df = build_risk_features(
                X,
                predicted_crowd
            )

            risk_columns = [
                "predicted_crowd",
                "predicted_crowd_level",
                "temp",
                "rain",
                "wind",
                "humidity",
                "weather_cat_num",
                "rain_intensity_num",
                "weather_severity",
                "heavy_rain_flag",
                "storm_flag",
                "day_of_week",
                "is_weekend",
                "month",
                "seasonal_factor",
                "day_type_num",
                "shrine_num",
                "darshan_duration",
                "peak_hour_flag",
                "lag_1",
                "lag_3",
                "lag_7",
                "rolling_mean_7",
                "trend",
                "predicted_temple_pressure",
                "predicted_crowd_weather_interaction",
                "predicted_weekend_crowd_interaction",
                "predicted_rain_crowd_interaction",
                "predicted_final_risk_signal"
            ]

            risk_df = risk_df[risk_columns]

            risk_prediction = int(
                risk_model.predict(risk_df)[0]
            )

            probs = risk_model.predict_proba(risk_df)[0]

            risk_text = {
                0: "Safe",
                1: "Moderate",
                2: "High"
            }.get(
                risk_prediction,
                "Unknown"
            )

            results.append(
                {
                    "Date": day_weather["date"],
                    "Temperature": round(day_weather["temperature"], 2),
                    "Humidity": round(day_weather["humidity"], 2),
                    "Wind": round(day_weather["wind_speed"], 2),
                    "Rain": round(day_weather["precipitation_probability"], 2),
                    "Visibility": round(day_weather["visibility"], 2),
                    "Crowd": int(predicted_crowd),
                    "Risk": risk_text,
                    "Safe_Prob": round(probs[0] * 100, 2),
                    "Moderate_Prob": round(probs[1] * 100, 2),
                    "High_Prob": round(probs[2] * 100, 2),
                    "High Risk Probability": round(probs[2] * 100, 2),
                }
            )

        forecast_df = pd.DataFrame(results)

        if forecast_df.empty:
            st.warning("No forecast data returned for the selected period.")
            st.stop()

        show_complete_weather_section(forecast_df)

    except Exception as e:
        st.exception(e)