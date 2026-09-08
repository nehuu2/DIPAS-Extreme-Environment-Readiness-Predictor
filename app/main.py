from flask import Flask, jsonify, request, send_from_directory
from sqlmodel import Session
from pydantic import ValidationError

from app.database import create_db_and_tables, engine
from app.models import ReadinessAssessment
from app.schemas import ReadinessInput
from app.services import calculate_readiness
from app.recommendations import generate_recommendations


# -----------------------------
# Flask Application
# -----------------------------

app = Flask(
    __name__,
    static_folder="../frontend",
    static_url_path=""
)


# -----------------------------
# Create Database and Tables
# -----------------------------

create_db_and_tables()


# -----------------------------
# Frontend
# -----------------------------

@app.route("/")
def home():
    return send_from_directory("../frontend", "index.html")


# -----------------------------
# Health Check
# -----------------------------

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy"
    }), 200


# -----------------------------
# Readiness Assessment
# -----------------------------

@app.route("/readiness", methods=["POST"])
def calculate_readiness_route():

    # Get JSON data from request
    data = request.get_json()

    # Check if JSON body exists
    if data is None:
        return jsonify({
            "error": "Invalid or missing JSON body"
        }), 400

    # -----------------------------
    # Validate Input
    # -----------------------------

    try:
        assessment_input = ReadinessInput.model_validate(data)

    except ValidationError as e:
        return jsonify({
            "error": "Validation error",
            "details": e.errors()
        }), 400

    # -----------------------------
    # Calculate Readiness
    # -----------------------------

    score, risk_level = calculate_readiness(
        assessment_input
    )

    # -----------------------------
    # Generate Recommendations
    # -----------------------------

    recommendations = generate_recommendations(
        assessment_input
    )

    # -----------------------------
    # Create Database Record
    # -----------------------------

    assessment = ReadinessAssessment(
        age=assessment_input.age,
        altitude=assessment_input.altitude,
        temperature=assessment_input.temperature,
        humidity=assessment_input.humidity,
        sleep_hours=assessment_input.sleep_hours,
        resting_heart_rate=assessment_input.resting_heart_rate,
        hydration_level=assessment_input.hydration_level,
        readiness_score=score,
        risk_level=risk_level
    )

    # -----------------------------
    # Save to SQLite Database
    # -----------------------------

    with Session(engine) as session:

        session.add(assessment)

        session.commit()

        session.refresh(assessment)

    # -----------------------------
    # Return Response
    # -----------------------------

    return jsonify({
        "message": "Readiness calculated and saved successfully",
        "id": assessment.id,
        "readiness_score": score,
        "risk_level": risk_level,
        "recommendations": recommendations
    }), 200


# -----------------------------
# Run Flask Application
# -----------------------------

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=8000,
        debug=True
    )