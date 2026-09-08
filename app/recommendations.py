def generate_recommendations(data):
    recommendations = []

    # --------------------------------
    # AGE
    # --------------------------------
    # Age is already validated in schemas.py
    # to be between 18 and 120.

    # --------------------------------
    # SLEEP
    # --------------------------------

    if data.sleep_hours < 4:
        recommendations.append(
            "Sleep duration is critically low. Get adequate rest before performing strenuous activities."
        )

    elif data.sleep_hours < 6:
        recommendations.append(
            "Sleep duration is low. Try to get at least 7 hours of sleep before extreme-environment exposure."
        )

    elif data.sleep_hours < 7:
        recommendations.append(
            "Try to get at least 7 hours of sleep for better physical readiness."
        )


    # --------------------------------
    # HYDRATION
    # --------------------------------

    if data.hydration_level <= 25:
        recommendations.append(
            "Hydration level is critically low. Rehydrate before exposure to extreme conditions."
        )

    elif data.hydration_level < 50:
        recommendations.append(
            "Hydration level is low. Maintain adequate hydration before and during activity."
        )

    elif data.hydration_level < 70:
        recommendations.append(
            "Increase hydration before exposure to extreme environmental conditions."
        )


    # --------------------------------
    # RESTING HEART RATE
    # --------------------------------

    if data.resting_heart_rate >= 110:
        recommendations.append(
            "Resting heart rate is very high. Avoid strenuous activity and monitor your condition carefully."
        )

    elif data.resting_heart_rate > 100:
        recommendations.append(
            "Resting heart rate is high. Consider taking adequate rest and monitor your condition."
        )

    elif data.resting_heart_rate > 90:
        recommendations.append(
            "Resting heart rate is elevated. Consider taking adequate rest before strenuous activity."
        )


    # --------------------------------
    # TEMPERATURE
    # --------------------------------

    if data.temperature >= 45:
        recommendations.append(
            "Extreme heat detected. Avoid prolonged exposure, take frequent breaks, and maintain hydration."
        )

    elif data.temperature > 40:
        recommendations.append(
            "Very high temperature detected. Take precautions against heat exposure and stay hydrated."
        )

    elif data.temperature > 35:
        recommendations.append(
            "High temperature detected. Take regular breaks and maintain adequate hydration."
        )

    elif data.temperature <= -20:
        recommendations.append(
            "Extreme cold detected. Use appropriate protective clothing and limit prolonged exposure."
        )

    elif data.temperature < 0:
        recommendations.append(
            "Low temperature detected. Use appropriate cold-weather protection and monitor for cold stress."
        )


    # --------------------------------
    # HUMIDITY
    # --------------------------------

    if data.humidity > 80:
        recommendations.append(
            "Very high humidity detected. Monitor heat stress carefully and maintain hydration."
        )

    elif data.humidity > 70:
        recommendations.append(
            "High humidity detected. Maintain hydration and take regular breaks during physical activity."
        )

    elif data.humidity < 20:
        recommendations.append(
            "Very low humidity detected. Maintain adequate hydration during exposure."
        )


    # --------------------------------
    # ALTITUDE
    # --------------------------------

    if data.altitude >= 4000:
        recommendations.append(
            "Very high altitude detected. Proper acclimatization and continuous monitoring are important."
        )

    elif data.altitude > 2500:
        recommendations.append(
            "High altitude detected. Allow adequate acclimatization before strenuous activity."
        )

    elif data.altitude > 1500:
        recommendations.append(
            "Elevated altitude detected. Monitor your condition and allow time for acclimatization."
        )


    # --------------------------------
    # MULTIPLE EXTREME CONDITIONS
    # --------------------------------

    extreme_conditions = 0

    if data.altitude >= 4000:
        extreme_conditions += 1

    if data.temperature >= 45 or data.temperature <= -20:
        extreme_conditions += 1

    if data.humidity > 80:
        extreme_conditions += 1

    if data.sleep_hours < 4:
        extreme_conditions += 1

    if data.resting_heart_rate >= 110:
        extreme_conditions += 1

    if data.hydration_level <= 25:
        extreme_conditions += 1


    if extreme_conditions >= 3:
        recommendations.append(
            "Multiple extreme factors detected. Consider postponing strenuous activity until conditions improve."
        )


    # --------------------------------
    # DEFAULT RECOMMENDATION
    # --------------------------------

    if not recommendations:
        recommendations.append(
            "Current conditions appear favorable. Continue monitoring your readiness."
        )


    return recommendations