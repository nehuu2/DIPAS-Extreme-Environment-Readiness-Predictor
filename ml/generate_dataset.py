import numpy as np
import pandas as pd


# Number of records
N = 5000

# Make results reproducible
np.random.seed(42)


# -----------------------------------
# Generate input features
# -----------------------------------

age = np.random.randint(18, 61, N)

altitude = np.random.uniform(0, 6000, N)

temperature = np.random.uniform(-20, 50, N)

humidity = np.random.uniform(20, 100, N)

sleep_hours = np.random.uniform(3, 10, N)

resting_heart_rate = np.random.uniform(50, 120, N)

hydration_level = np.random.uniform(30, 100, N)


# -----------------------------------
# Calculate a synthetic readiness score
# -----------------------------------

score = np.full(N, 100.0)


# Sleep penalty
score -= np.where(
    sleep_hours < 6,
    20,
    np.where(sleep_hours < 7, 10, 0)
)


# Hydration penalty
score -= np.where(
    hydration_level < 50,
    20,
    np.where(hydration_level < 70, 10, 0)
)


# Heart-rate penalty
score -= np.where(
    resting_heart_rate > 100,
    20,
    np.where(resting_heart_rate > 90, 10, 0)
)


# Temperature penalty
score -= np.where(
    temperature > 40,
    20,
    np.where(temperature > 35, 10, 0)
)


# Humidity penalty
score -= np.where(
    humidity > 80,
    10,
    0
)


# Altitude penalty
score -= np.where(
    altitude > 4000,
    20,
    np.where(altitude > 2500, 10, 0)
)


# Keep score between 0 and 100
score = np.clip(score, 0, 100)


# -----------------------------------
# Create DataFrame
# -----------------------------------

df = pd.DataFrame({
    "age": age,
    "altitude": altitude,
    "temperature": temperature,
    "humidity": humidity,
    "sleep_hours": sleep_hours,
    "resting_heart_rate": resting_heart_rate,
    "hydration_level": hydration_level,
    "readiness_score": score
})


# -----------------------------------
# Save dataset
# -----------------------------------

df.to_csv(
    "data/readiness_dataset.csv",
    index=False
)


print("Dataset created successfully!")
print(f"Number of records: {len(df)}")
print("\nFirst 5 records:")
print(df.head())

print("\nDataset saved to:")
print("data/readiness_dataset.csv")