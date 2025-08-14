# 🖥️ Abschlussprojekt: Empfehlung von Mac-Rechnern in Unternehmen

## 📌 Projektbeschreibung
Dieses Projekt untersucht, in welchen Unternehmensszenarien der Einsatz von **Mac-Rechnern** sinnvoll ist.  
Dazu wurde ein **Machine-Learning-Modell** entwickelt, das auf Basis von Mitarbeiterprofilen eine **Empfehlung** ausspricht.  
Die Ergebnisse werden in einem **interaktiven Dashboard** (Streamlit) dargestellt.

---

## 🎯 Hypothese
> *"Mitarbeiter mit kreativen Aufgaben, hoher Mobilität und Bedarf an Design-Tools profitieren häufiger von einem Mac als andere Mitarbeitergruppen."*

Wir prüfen, ob sich diese Annahme **datenbasiert** bestätigen lässt und welche weiteren Faktoren relevant sind.

---

## 🗂️ Projektziele
- Entwicklung eines Klassifikationsmodells zur Vorhersage der Mac-Eignung
- Visualisierung der Ergebnisse in einem interaktiven Dashboard
- Erklärbarkeit der Modellentscheidungen (Feature Importance)
- Ableitung klarer Handlungsempfehlungen für die IT-Abteilung

---

## 🧠 Methodik
1. **Datengenerierung**  
   - Synthetischer Datensatz mit typischen Unternehmensprofilen  
   - Features: Rolle, Software-Nutzung, Mobilität, Sicherheitsanforderungen, Budget, OS-Präferenz  
2. **Modelltraining**  
   - RandomForestClassifier (scikit-learn)  
   - Cross-Validation zur Performance-Bewertung  
3. **Erklärbarkeit**  
   - Permutation Feature Importance zur Bestimmung der wichtigsten Einflussfaktoren  
4. **Dashboard-Entwicklung**  
   - Streamlit-App mit Eingabeformular, Vorhersage und Visualisierung

---

## 🛠️ Technologie-Stack
- **Programmiersprache:** Python 3.x
- **Bibliotheken:**  
  - `pandas`, `numpy` – Datenverarbeitung  
  - `scikit-learn` – Machine Learning  
  - `streamlit` – Dashboard  
  - `matplotlib`, `seaborn` – Visualisierung
- **Entwicklungsumgebung:** macOS / venv
- **Modell:** Random Forest Classifier

---

## 📊 Workflow
```plaintext
Datenaufbereitung → Modelltraining → Evaluation → Dashboard → Empfehlung

## Daten
data_gen.py
train_model.py
app.py
mac_dataset.csv
model.joblib
requirements.txt