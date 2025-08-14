"""Erzeugt einen synthetischen Datensatz zur Entscheidung 'Mac empfehlen'."""

import random
import pandas as pd
import numpy as np

random.seed(42)
np.random.seed(42)

roles = ["Developer", "Designer", "Marketing", "Management", "Support", "DataScientist"]
os_pref = ["mac", "windows", "linux", "none"]
security_levels = ["low", "medium", "high"]
mobility_levels = ["low", "medium", "high"]
budget_levels = ["low", "medium", "high"]

def make_row():
    role = random.choice(roles)
    uses_design = 1 if role == "Designer" or random.random() < 0.1 else 0
    uses_office = 1 if role in ["Management", "Marketing", "Support"] or random.random() < 0.6 else 0
    requires_windows_only = 1 if role == "Support" and random.random() < 0.3 else (1 if random.random() < 0.12 else 0)
    mobility = random.choice(mobility_levels)
    security = random.choice(security_levels)
    budget = random.choice(budget_levels)
    os_preference = random.choice(os_pref)

    # Heuristische Zielvariable: Designer + kein Windows-only -> Mac hoch
    score = 0
    if uses_design: score += 2
    if requires_windows_only: score -= 3
    if os_preference == "mac": score += 2
    if mobility == "high": score += 1
    if security == "high": score += 0.5
    if budget == "low": score -= 1

    recommend_mac = 1 if score > 0.5 else 0

    return {
        "role": role,
        "uses_design_tools": uses_design,
        "uses_office_apps": uses_office,
        "requires_windows_only_apps": requires_windows_only,
        "mobility": mobility,
        "security_sensitivity": security,
        "budget_sensitivity": budget,
        "preferred_os": os_preference,
        "recommend_mac": recommend_mac
    }

def generate(n=1000, out_csv="mac_dataset.csv"):
    rows = [make_row() for _ in range(n)]
    df = pd.DataFrame(rows)
    df.to_csv(out_csv, index=False)
    print(f"Wrote {len(df)} rows to {out_csv}")

if __name__ == "__main__":
    generate(2000, "mac_dataset.csv")