from app.schemas import ReadinessInput
from app.recommendations import generate_recommendations


# Test user input
data = ReadinessInput(
    age=24,
    altitude=2500,
    temperature=32,
    humidity=65,
    sleep_hours=7,
    resting_heart_rate=72,
    hydration_level=80
)


# Generate recommendations
recommendations = generate_recommendations(data)


print("Recommendations:")

for recommendation in recommendations:
    print("-", recommendation)