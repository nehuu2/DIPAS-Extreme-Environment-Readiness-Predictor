from flask import Flask, jsonify, request, send_from_directory
from sqlmodel import Session, select
from pydantic import ValidationError

from app.database import create_db_and_tables, engine
from app.models import User, ReadinessAssessment
from app.schemas import (
    ReadinessInput,
    UserCreate,
    UserUpdate
)
from app.services import calculate_readiness
from app.recommendations import generate_recommendations


# ============================================================
# Flask Application
# ============================================================

app = Flask(
    __name__,
    static_folder="../frontend",
    static_url_path=""
)


# ============================================================
# Create Database and Tables
# ============================================================

create_db_and_tables()


# ============================================================
# Frontend
# ============================================================

@app.route("/")
def home():
    return send_from_directory("../frontend", "index.html")


# ============================================================
# Health Check
# ============================================================

@app.route("/health", methods=["GET"])
def health_check():

    return jsonify({
        "status": "healthy"
    }), 200


# ============================================================
# USER PROFILE APIs
# ============================================================


# ------------------------------------------------------------
# Create User
# POST /api/v1/users
# ------------------------------------------------------------

@app.route("/api/v1/users", methods=["POST"])
def create_user():

    # Get JSON data
    data = request.get_json()

    # Check JSON body
    if data is None:
        return jsonify({
            "error": "Invalid or missing JSON body"
        }), 400

    # Validate input
    try:
        user_input = UserCreate.model_validate(data)

    except ValidationError as e:

        return jsonify({
            "error": "Validation error",
            "details": e.errors()
        }), 400

    # Database operation
    with Session(engine) as session:

        # Check duplicate email
        statement = select(User).where(
            User.email == user_input.email
        )

        existing_user = session.exec(statement).first()

        if existing_user:

            return jsonify({
                "error": "A user with this email already exists"
            }), 409

        # Create user
        user = User(
            name=user_input.name,
            email=user_input.email
        )

        session.add(user)

        session.commit()

        session.refresh(user)

    # Response
    return jsonify({
        "message": "User created successfully",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at.isoformat()
        }
    }), 201


# ------------------------------------------------------------
# Get User
# GET /api/v1/users/<user_id>
# ------------------------------------------------------------

@app.route("/api/v1/users/<int:user_id>", methods=["GET"])
def get_user(user_id):

    with Session(engine) as session:

        user = session.get(User, user_id)

        if user is None:

            return jsonify({
                "error": "User not found"
            }), 404

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "created_at": user.created_at.isoformat()
    }), 200


# ------------------------------------------------------------
# Update User
# PUT /api/v1/users/<user_id>
# ------------------------------------------------------------

@app.route("/api/v1/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):

    # Get JSON data
    data = request.get_json()

    if data is None:

        return jsonify({
            "error": "Invalid or missing JSON body"
        }), 400

    # Validate input
    try:
        user_input = UserUpdate.model_validate(data)

    except ValidationError as e:

        return jsonify({
            "error": "Validation error",
            "details": e.errors()
        }), 400

    with Session(engine) as session:

        # Find user
        user = session.get(User, user_id)

        if user is None:

            return jsonify({
                "error": "User not found"
            }), 404

        # Check duplicate email
        statement = select(User).where(
            User.email == user_input.email,
            User.id != user_id
        )

        existing_user = session.exec(statement).first()

        if existing_user:

            return jsonify({
                "error": "Another user already uses this email"
            }), 409

        # Update user
        user.name = user_input.name
        user.email = user_input.email

        session.add(user)

        session.commit()

        session.refresh(user)

    return jsonify({
        "message": "User profile updated successfully",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at.isoformat()
        }
    }), 200


# ============================================================
# READINESS ASSESSMENT
# ============================================================


# ------------------------------------------------------------
# Calculate Readiness
# POST /readiness
# ------------------------------------------------------------

@app.route("/readiness", methods=["POST"])
def calculate_readiness_route():

    # Get JSON data
    data = request.get_json()

    # Check if JSON body exists
    if data is None:

        return jsonify({
            "error": "Invalid or missing JSON body"
        }), 400

    # --------------------------------------------------------
    # Validate Input
    # --------------------------------------------------------

    try:

        assessment_input = ReadinessInput.model_validate(data)

    except ValidationError as e:

        return jsonify({
            "error": "Validation error",
            "details": e.errors()
        }), 400

    # --------------------------------------------------------
    # Calculate Readiness
    # --------------------------------------------------------

    score, risk_level = calculate_readiness(
        assessment_input
    )

    # --------------------------------------------------------
    # Generate Recommendations
    # --------------------------------------------------------

    recommendations = generate_recommendations(
        assessment_input
    )

    # --------------------------------------------------------
    # Create Database Record
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Save to SQLite Database
    # --------------------------------------------------------

    with Session(engine) as session:

        session.add(assessment)

        session.commit()

        session.refresh(assessment)

    # --------------------------------------------------------
    # Return Response
    # --------------------------------------------------------

    return jsonify({
        "message": "Readiness calculated and saved successfully",
        "id": assessment.id,
        "readiness_score": score,
        "risk_level": risk_level,
        "recommendations": recommendations
    }), 200


# ============================================================
# Run Flask Application
# ============================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=8000,
        debug=True
    )