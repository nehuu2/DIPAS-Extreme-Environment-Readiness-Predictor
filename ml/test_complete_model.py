import joblib
import pandas as pd

from app.schemas import ReadinessInput
from app.recommendations import generate_recommendations


# -----------------------------------
# Load trained ML model
# -----------------------------------

model = joblib.load("ml/readiness_model.pkl")


# -----------------------------------
# New user input
# -----------------------------------

data = ReadinessInput(
    age=24,
    altitude=2500,
    temperature=32,
    humidity=65,
    sleep_hours=7,
    resting_heart_rate=72,
    hydration_level=80
)


# -----------------------------------
# Prepare data for ML model
# -----------------------------------

input_data = pd.DataFrame([{
    "age": data.age,
    "altitude": data.altitude,
    "temperature": data.temperature,
    "humidity": data.humidity,
    "sleep_hours": data.sleep_hours,
    "resting_heart_rate": data.resting_heart_rate,
    "hydration_level": data.hydration_level
}])


# -----------------------------------
# Predict readiness score
# -----------------------------------

prediction = model.predict(input_data)

readiness_score = round(prediction[0], 2)


# -----------------------------------
# Determine risk level
# -----------------------------------

if readiness_score >= 75:
    risk_level = "Low"

elif readiness_score >= 50:
    risk_level = "Moderate"

else:
    risk_level = "High"


# -----------------------------------
# Generate recommendations
# -----------------------------------

recommendations = generate_recommendations(data)


# -----------------------------------
# Display final result
# -----------------------------------

print("\n" + "=" * 40)
print("DIPAS READINESS ASSESSMENT")
print("=" * 40)

print("Readiness Score:", readiness_score)
print("Risk Level:", risk_level)

print("\nRecommendations:")

for recommendation in recommendations:
    print("-", recommendation)

print("=" * 40)