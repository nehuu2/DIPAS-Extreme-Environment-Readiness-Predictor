from sqlmodel import SQLModel, create_engine, Session, text

from app.models import User, ReadinessAssessment


DATABASE_URL = "sqlite:///readiness.db"

engine = create_engine(
    DATABASE_URL,
    echo=True
)


def create_db_and_tables():
    # Create new tables if they don't exist
    SQLModel.metadata.create_all(engine)

    # Check whether user_id already exists
    with engine.connect() as connection:
        result = connection.execute(
            text("PRAGMA table_info(readinessassessment)")
        )

        columns = [row[1] for row in result]

        if "user_id" not in columns:
            connection.execute(
                text(
                    "ALTER TABLE readinessassessment "
                    "ADD COLUMN user_id INTEGER"
                )
            )

            connection.commit()

            print("Added user_id column to readinessassessment table.")
        else:
            print("user_id column already exists.")