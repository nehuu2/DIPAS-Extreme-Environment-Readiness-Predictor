import joblib
import pandas as pd


# Load trained ML model
model = joblib.load("ml/readiness_model.pkl")


def calculate_readiness(data):

    # -----------------------------
    # Prepare input for ML model
    # -----------------------------

    input_data = pd.DataFrame([{
        "age": data.age,
        "altitude": data.altitude,
        "temperature": data.temperature,
        "humidity": data.humidity,
        "sleep_hours": data.sleep_hours,
        "resting_heart_rate": data.resting_heart_rate,
        "hydration_level": data.hydration_level
    }])

    # -----------------------------
    # ML Prediction
    # -----------------------------

    prediction = model.predict(input_data)

    score = float(prediction[0])

    # Keep score between 0 and 100
    score = max(0, min(score, 100))

    score = round(score, 2)

    # -----------------------------
    # Safety Override Rules
    # -----------------------------
    # These rules prevent the ML model
    # from assigning Low risk to clearly
    # extreme conditions.

    safety_risk = None

    # Very high altitude
    if data.altitude >= 4000:
        safety_risk = "High"

    # Very high temperature
    elif data.temperature >= 45:
        safety_risk = "High"

    # Very low temperature
    elif data.temperature <= -20:
        safety_risk = "High"

    # Very high resting heart rate
    elif data.resting_heart_rate >= 110:
        safety_risk = "High"

    # Very low hydration
    elif data.hydration_level <= 25:
        safety_risk = "High"

    # Extremely low sleep
    elif data.sleep_hours < 4:
        safety_risk = "High"

    # --------------------------------
    # Determine Final Risk Level
    # --------------------------------

    if safety_risk == "High":
        risk_level = "High"

    elif score >= 75:
        risk_level = "Low"

    elif score >= 50:
        risk_level = "Moderate"

    else:
        risk_level = "High"

    return score, risk_level