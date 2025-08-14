
"""Streamlit App zur Interaktion mit dem Modell."""
import streamlit as st
import pandas as pd
import joblib
from sklearn.inspection import permutation_importance

MODEL_PATH = "model.joblib"

@st.cache_resource
def load_model(path=MODEL_PATH):
    return joblib.load(path)

st.set_page_config(page_title="Mac-Empfehlungs-Tool", layout="centered")

st.title("Mac-Empfehlungs-Tool für Unternehmen")
st.markdown("Gib Arbeitsplatz-Merkmale ein und erhalte eine Empfehlung, ob ein Mac sinnvoll ist.")

# Sidebar: Eingaben
st.sidebar.header("Eingaben")
role = st.sidebar.selectbox("Rolle", ["Developer", "Designer", "Marketing", "Management", "Support", "DataScientist"])
uses_design = st.sidebar.radio("Verwendet Design-Tools?", ("Ja", "Nein")) == "Ja"
uses_office = st.sidebar.radio("Verwendet Office-Apps (Word/Excel/Outlook)?", ("Ja", "Nein")) == "Ja"
requires_windows = st.sidebar.radio("Benötigt Windows-Only Apps?", ("Ja", "Nein")) == "Ja"
mobility = st.sidebar.selectbox("Mobilität", ["low", "medium", "high"])
security = st.sidebar.selectbox("Sicherheitsanforderung", ["low", "medium", "high"])
budget = st.sidebar.selectbox("Budgetempfindlichkeit", ["low", "medium", "high"])
pref_os = st.sidebar.selectbox("Betriebssystempräferenz", ["mac", "windows", "linux", "none"])

if st.sidebar.button("Vorhersage"):
    model = load_model()

    # Eingabe-Datenframe
    input_df = pd.DataFrame([{
        "role": role,
        "uses_design_tools": int(uses_design),
        "uses_office_apps": int(uses_office),
        "requires_windows_only_apps": int(requires_windows),
        "mobility": mobility,
        "security_sensitivity": security,
        "budget_sensitivity": budget,
        "preferred_os": pref_os
    }])

    # Spaltenprüfung und Reihenfolge aus Modell übernehmen
    expected_cols = model.feature_names_in_
    missing = set(expected_cols) - set(input_df.columns)
    if missing:
        st.error(f"Fehlende Spalten im Eingabe-DataFrame: {missing}")
        st.stop()
    input_df = input_df.reindex(columns=expected_cols)

    # Vorhersage
    pred_proba = model.predict_proba(input_df)[:, 1][0]
    pred = model.predict(input_df)[0]

    st.subheader("Ergebnis")
    st.metric("Wahrscheinlichkeit für 'Mac empfohlen' (%)", f"{pred_proba * 100:.1f}%")
    st.write("Empfehlung:", "✅ Mac empfohlen" if pred == 1 else "❌ Mac nicht empfohlen")

    # Feature Importances (Permutation)
    try:
        df_full = pd.read_csv("mac_dataset.csv")
        X = df_full.drop(columns=["recommend_mac"])
        y = df_full["recommend_mac"]

        # Sample für schnelleres Rechnen
        X_sample = X.sample(n=min(300, len(X)), random_state=42)
        y_sample = y.loc[X_sample.index]

        # Preprocessor & Feature-Namen aus Pipeline
        preproc = model.named_steps["preproc"]
        feature_names = preproc.get_feature_names_out()

        # Transformierte Daten
        X_transformed = preproc.transform(X_sample)

        # permutation_importance nur auf Klassifikator anwenden
        r = permutation_importance(
            model.named_steps["clf"],
            X_transformed,
            y_sample,
            n_repeats=10,
            random_state=42,
            n_jobs=1
        )

        # DataFrame bauen
        imp_df = pd.DataFrame({
            "feature": feature_names,
            "importance": r.importances_mean
        }).sort_values("importance", ascending=False).head(10)

        st.subheader("Top Feature-Importances (Permutation)")
        st.table(imp_df.reset_index(drop=True))
    except Exception as e:
        st.write("Feature-Importances konnten nicht berechnet werden:", e)