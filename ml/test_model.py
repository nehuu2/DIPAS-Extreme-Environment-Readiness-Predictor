import joblib
import pandas as pd


# Load trained model
model = joblib.load("ml/readiness_model.pkl")


# New user input
new_data = pd.DataFrame([{
    "age": 24,
    "altitude": 2500,
    "temperature": 32,
    "humidity": 65,
    "sleep_hours": 7,
    "resting_heart_rate": 72,
    "hydration_level": 80
}])


# Make prediction
prediction = model.predict(new_data)


# Display result
print("Predicted Readiness Score:", round(prediction[0], 2))