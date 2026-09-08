from sqlmodel import Field, SQLModel


class ReadinessInput(SQLModel):
    age: int = Field(ge=18, le=120)

    altitude: float = Field(ge=0)

    temperature: float = Field(ge=-50, le=60)

    humidity: float = Field(ge=0, le=100)

    sleep_hours: float = Field(ge=0, le=24)

    resting_heart_rate: float = Field(gt=0)

    hydration_level: float = Field(ge=0, le=100)


class ReadinessOutput(SQLModel):
    id: int
    readiness_score: float = Field(ge=0, le=100)
    risk_level: str