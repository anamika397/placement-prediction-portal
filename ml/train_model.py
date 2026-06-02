import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

data = pd.read_csv("dataset/placement_data.csv")

X = data[
    [
        "CGPA",
        "Aptitude",
        "Coding",
        "Communication",
        "Projects"
    ]
]

y = data["Placed"]

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

joblib.dump(
    model,
    "ml/placement_model.pkl"
)

print("Model trained successfully!")