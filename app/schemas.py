from pydantic import BaseModel, EmailStr, Field


# -----------------------------
# Readiness Input Schema
# -----------------------------

class ReadinessInput(BaseModel):
    age: int = Field(gt=0, le=120)

    altitude: float = Field(ge=0)

    temperature: float

    humidity: float = Field(ge=0, le=100)

    sleep_hours: float = Field(ge=0, le=24)

    resting_heart_rate: float = Field(gt=0)

    hydration_level: float = Field(ge=0, le=100)


# -----------------------------
# Readiness Output Schema
# -----------------------------

class ReadinessOutput(BaseModel):
    readiness_score: float
    risk_level: str
    recommendations: list[str]


# -----------------------------
# User Create Schema
# -----------------------------

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)

    email: EmailStr


# -----------------------------
# User Update Schema
# -----------------------------

class UserUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=100)

    email: EmailStr


# -----------------------------
# User Output Schema
# -----------------------------

class UserOutput(BaseModel):
    id: int
    name: str
    email: str
    created_at: str