🛕 Smart AI-Based Chardham Yatra Assistance System

An AI-powered decision support system designed to enhance the safety, planning, and travel experience of pilgrims undertaking the Chardham Yatra. The system combines crowd forecasting, weather intelligence, risk assessment, and recommendation generation to provide real-time guidance for the four sacred shrines: Kedarnath, Badrinath, Gangotri, and Yamunotri.

📌 Project Overview

The Chardham Yatra attracts millions of pilgrims every year and faces several challenges including:

Sudden weather changes
Heavy rainfall and landslides
Road blockages
Overcrowding and long waiting times
Difficulty choosing the safest day to travel

This project uses Machine Learning and AI techniques to predict:

Future pilgrim crowd levels
Travel risk levels
Best days to visit
Personalized travel recommendations

The system serves as an intelligent assistant that helps pilgrims make safer and more informed travel decisions.

🎯 Objectives
Predict daily crowd levels at each shrine.
Assess pilgrimage risk using weather and crowd conditions.
Recommend the safest travel days.
Provide real-time insights through a user-friendly dashboard.
Improve pilgrim safety and reduce congestion.
🏔️ Supported Shrines
Kedarnath
Badrinath
Gangotri
Yamunotri
🏗️ System Architecture
Weather API
      │
      ▼
Weather Data Processing
      │
      ▼
Feature Engineering
      │
      ├───────────────► Crowd Prediction Model (XGBoost)
      │
      ▼
Risk Prediction Model (Random Forest)
      │
      ▼
Recommendation Engine
      │
      ▼
Streamlit Dashboard
📊 Core Features
1. Crowd Prediction Engine

Predicts future pilgrim footfall using:

Historical crowd trends
Weather conditions
Seasonal patterns
Weekly crowd behavior
Shrine-specific patterns
Model Used
XGBoost Regressor
Output
Predicted Crowd Count
Crowd Level Classification:
Low
Medium
High
2. Risk Assessment Engine

Determines travel safety using:

Crowd pressure
Rainfall intensity
Weather severity
Storm conditions
Weekend rush
Temple congestion
Model Used
Random Forest Classifier
Risk Categories
Risk Level	Meaning
Safe	Suitable for travel
Moderate	Travel with caution
Risky	High risk, avoid if possible
3. Weather Intelligence Module

Processes weather forecasts and derives:

Weather Category
Rain Intensity
Weather Severity Score
Heavy Rain Detection
Storm Detection
Weather Categories
Value	Category
0	Clear
1	Rain
2	Storm
4. Recommendation Engine

Provides:

Best day to visit
Crowd comparison
Risk comparison
Shrine recommendations
Safety alerts

Decision logic considers:

Predicted crowd
Weather severity
Risk probability
Weekend congestion
🧠 Feature Engineering

The system transforms raw data into meaningful decision signals.

Weather Features
Feature	Purpose
weather_cat_num	Weather condition category
rain_intensity_num	Rain severity
weather_severity	Combined weather risk score
heavy_rain_flag	Heavy rainfall indicator
storm_flag	Storm indicator
Crowd Features
Feature	Purpose
crowd_level_num	Crowd pressure classification
temple_pressure	Temple congestion score
trend	Crowd growth trend
Time Features
Feature	Purpose
day_of_week	Weekly pattern
is_weekend	Weekend detection
seasonal_factor	Seasonal variation
month	Monthly behavior
Historical Features
Feature	Purpose
lag_1	Previous day crowd
lag_3	Previous 3-day crowd
lag_7	Previous week crowd
rolling_mean_7	Weekly average crowd
Interaction Features
Feature	Purpose
crowd_weather_interaction	Crowd + weather impact
weekend_crowd_interaction	Weekend crowd effect
temple_pressure	Temple congestion
final_risk_signal	Overall danger indicator
📈 Machine Learning Models
Crowd Forecasting Model
Parameter	Value
Algorithm	XGBoost Regressor
Trees	400
Max Depth	7
Learning Rate	0.05
Subsample	0.8
Risk Prediction Model
Parameter	Value
Algorithm	Random Forest
Trees	300
Max Depth	10
Min Samples Split	5
Min Samples Leaf	3
Class Weight	Balanced
📊 Model Evaluation

The project includes extensive evaluation through:

Performance Metrics
Accuracy
Precision
Recall
F1 Score
MAE
RMSE
R² Score
WMAPE
Explainability
SHAP Analysis
Feature Importance
Confusion Matrix
ROC Curves
Advanced Validation
Cross-Dataset Validation
Generalization Testing
Robustness Analysis
Ablation Studies
⚡ Edge vs Cloud Analysis

The system compares:

Edge Deployment
Faster response
Lower latency
Better real-time performance
Cloud Deployment
Higher computation power
Scalability
Centralized management

The project includes simulated latency experiments to evaluate deployment feasibility.

🌦️ Future Weather Forecasting

Weather forecasts are fetched using:

Tomorrow.io Weather API

Forecast parameters:

Temperature
Rainfall
Humidity
Wind Speed
Weather Codes

The forecast data is converted into model-ready features before prediction.

📂 Project Structure
Smart-AI-Chardham-Yatra/
│
├── data/
│   ├── raw_data.csv
│   ├── processed_data.csv
│
├── models/
│   ├── crowd_xgb_model.pkl
│   ├── risk_rf_model.pkl
│
├── notebooks/
│   ├── Final_project_model.ipynb
│
├── app/
│   ├── streamlit_app.py
│
├── outputs/
│   ├── final_future_prediction_output.csv
│   ├── graphs/
│
├── README.md
│
└── requirements.txt
🚀 Installation

Clone the repository:

git clone https://github.com/yourusername/smart-ai-chardham-yatra.git

cd smart-ai-chardham-yatra

Install dependencies:

pip install -r requirements.txt

Run the application:

streamlit run app.py
🖥️ Dashboard Features

The Streamlit dashboard provides:

User Inputs
Select Shrine
Select Travel Date
View Future Predictions
Outputs
Predicted Crowd Count
Crowd Level
Risk Level
Risk Probabilities
Weather Conditions
Best Day Recommendation
Safety Suggestions
🔮 Future Enhancements
Live Traffic Integration
Landslide Prediction Module
Route Optimization
Emergency Alert System
Mobile Application
Multi-language Support
GPS-based Personalized Assistance
Real-Time Crowd Monitoring
🏆 Key Technologies
Python
Pandas
NumPy
Scikit-Learn
XGBoost
SHAP
Streamlit
Matplotlib
Seaborn
Tomorrow.io API
👨‍💻 Contributors
Gautam Rawat
Shivam Sharma
Saloni Goel
📜 License

This project is developed for academic and research purposes as part of a Smart AI-Based Chardham Yatra Assistance System.

⭐ Project Summary

This system combines Machine Learning, Weather Intelligence, Crowd Analytics, and Risk Prediction to create a comprehensive pilgrimage assistance platform. By forecasting crowd levels and identifying potential travel risks, it helps pilgrims make safer, smarter, and more informed decisions throughout the Chardham Yatra journey.
