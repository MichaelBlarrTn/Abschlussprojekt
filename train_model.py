"""Trainieren eines RandomForest-Klassifikators und speichern des Modells."""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score
import joblib

RANDOM_STATE = 42
DATA_PATH = "mac_dataset.csv"
MODEL_PATH = "model.joblib"

def load_data(path=DATA_PATH):
    df = pd.read_csv(path)
    return df

def build_pipeline():
    cat_cols = ["role", "mobility", "security_sensitivity", "budget_sensitivity", "preferred_os"]
    num_cols = ["uses_design_tools", "uses_office_apps", "requires_windows_only_apps"]

    preproc = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_cols),
            ("num", "passthrough", num_cols)
        ],
        remainder="drop"
    )
    clf = RandomForestClassifier(n_estimators=200, random_state=RANDOM_STATE, n_jobs=1)
    pipe = Pipeline(steps=[("preproc", preproc), ("clf", clf)])
    return pipe

def main():
    df = load_data()
    x = df.drop(columns=["recommend_mac"])
    y = df["recommend_mac"]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y)

    pipe = build_pipeline()
    pipe.fit(x_train, y_train)

    y_pred  = pipe.predict(x_test)
    y_proba = pipe.predict_proba(x_test)[:,1]

    print("Accuracy:", accuracy_score(y_test, y_pred))
    try:
        print("ROC AUC:", roc_auc_score(y_test, y_proba))
    except Exception:
        pass
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

    joblib.dump(pipe, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    main()
