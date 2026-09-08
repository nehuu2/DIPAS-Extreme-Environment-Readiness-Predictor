from datetime import datetime

from sqlmodel import Field, SQLModel


class ReadinessAssessment(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    age: int = Field(gt=0, le=120)

    altitude: float = Field(ge=0)

    temperature: float

    humidity: float = Field(ge=0, le=100)

    sleep_hours: float = Field(ge=0, le=24)

    resting_heart_rate: float = Field(gt=0)

    hydration_level: float = Field(ge=0, le=100)

    readiness_score: float = Field(ge=0, le=100)

    risk_level: str

    created_at: datetime = Field(default_factory=datetime.utcnow)