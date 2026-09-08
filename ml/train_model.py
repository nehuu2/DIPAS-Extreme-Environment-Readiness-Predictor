import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# -----------------------------------
# Load dataset
# -----------------------------------

df = pd.read_csv("data/readiness_dataset.csv")


# -----------------------------------
# Separate features and target
# -----------------------------------

X = df.drop("readiness_score", axis=1)
y = df["readiness_score"]


# -----------------------------------
# Train-test split
# -----------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# -----------------------------------
# Create models
# -----------------------------------

models = {
    "Linear Regression": LinearRegression(),

    "Random Forest": RandomForestRegressor(
        n_estimators=100,
        random_state=42
    ),

    "Gradient Boosting": GradientBoostingRegressor(
        random_state=42
    )
}


# -----------------------------------
# Train and evaluate models
# -----------------------------------

for name, model in models.items():

    print("\n" + "=" * 50)
    print(name)
    print("=" * 50)

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)

    rmse = mean_squared_error(
        y_test,
        predictions
    ) ** 0.5

    r2 = r2_score(y_test, predictions)

    print("MAE :", round(mae, 2))
    print("RMSE:", round(rmse, 2))
    print("R2  :", round(r2, 4))


# -----------------------------------
# Train final Gradient Boosting model
# -----------------------------------

final_model = GradientBoostingRegressor(
    random_state=42
)

final_model.fit(X_train, y_train)


# -----------------------------------
# Save trained model
# -----------------------------------

joblib.dump(
    final_model,
    "ml/readiness_model.pkl"
)


print("\n" + "=" * 50)
print("Final model saved successfully!")
print("=" * 50)

print("Model: Gradient Boosting")
print("Location: ml/readiness_model.pkl")