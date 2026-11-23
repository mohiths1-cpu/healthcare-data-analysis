"""Generate a simulated healthcare dataset for the analysis application.

The data is entirely synthetic (no real patients). Realistic relationships
are built in (e.g. blood pressure rises with age and BMI) and typical data
quality problems are deliberately injected so that the preprocessing module
has real work to do: missing values, duplicate rows, inconsistent labels,
text in numeric columns and impossible values.

Usage:
    python data/generate_dataset.py
"""
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 42
N_PATIENTS = 300
OUTPUT_PATH = Path(__file__).resolve().parent / "healthcare_patients.csv"


def _simulate_clean(n, rng):
    """Create a clean synthetic patient table with correlated health metrics.

    Parameters
    ----------
    n : int
        Number of patients.
    rng : numpy.random.Generator
        Random number generator (seeded for reproducibility).

    Returns
    -------
    pandas.DataFrame
        Clean synthetic records.
    """
    age = np.clip(rng.normal(48, 16, n), 18, 90).round().astype(int)
    gender = rng.choice(["Male", "Female"], n)
    region = rng.choice(
        ["North", "South", "East", "West", "Central"], n,
        p=[0.22, 0.24, 0.18, 0.22, 0.14],
    )
    smoker = rng.choice(["Yes", "No"], n, p=[0.22, 0.78])
    activity = rng.choice(["Low", "Moderate", "High"], n, p=[0.40, 0.40, 0.20])

    bmi = np.clip(rng.normal(25.5, 4.2, n) + 0.04 * (age - 48), 15, 45)
    smoke_flag = (smoker == "Yes").astype(int)
    high_act = (activity == "High").astype(int)

    systolic = (112 + 0.45 * age + 0.9 * (bmi - 25) + 5 * smoke_flag
                - 4 * high_act + rng.normal(0, 10, n))
    diastolic = 0.5 * systolic + 18 + rng.normal(0, 5, n)
    glucose = (90 + 0.35 * age + 1.4 * (bmi - 25)
               + rng.normal(0, 17, n))
    cholesterol = 150 + 0.6 * age + 1.5 * bmi + rng.normal(0, 25, n)

    p_diabetes = 1 / (1 + np.exp(-(glucose - 128) / 10))
    diabetes = (rng.random(n) < p_diabetes).astype(int)
    hypertension = (systolic >= 140).astype(int)

    days = rng.poisson(1.2 + 2.0 * diabetes + 1.5 * hypertension + age / 40)
    visit_date = pd.to_datetime("2024-01-01") + pd.to_timedelta(
        rng.integers(0, 365, n), unit="D")

    return pd.DataFrame({
        "patient_id": [f"P{1000 + i}" for i in range(n)],
        "age": age,
        "gender": gender,
        "region": region,
        "bmi": bmi.round(1),
        "systolic_bp": systolic.round().astype(int),
        "diastolic_bp": diastolic.round().astype(int),
        "glucose": glucose.round(1),
        "cholesterol": cholesterol.round(1),
        "smoker": smoker,
        "physical_activity": activity,
        "visit_date": visit_date.strftime("%Y-%m-%d"),
        "hospital_stay_days": days,
        "diabetes": diabetes,
        "hypertension": hypertension,
    })


def _inject_quality_issues(df, rng):
    """Add realistic data-quality problems to a clean table.

    Parameters
    ----------
    df : pandas.DataFrame
        Clean table from ``_simulate_clean``.
    rng : numpy.random.Generator
        Random number generator.

    Returns
    -------
    pandas.DataFrame
        Table containing missing values, mixed labels, text in numeric
        columns, impossible values and duplicate rows.
    """
    df = df.copy()
    n = len(df)

    # Missing values in several columns.
    for col, k in [("bmi", 10), ("glucose", 8), ("cholesterol", 8),
                   ("systolic_bp", 5), ("smoker", 5), ("region", 4)]:
        df.loc[rng.choice(n, k, replace=False), col] = np.nan

    # Inconsistent labels (case, abbreviations, whitespace).
    df["gender"] = df["gender"].astype(object)
    idx = rng.choice(n, 40, replace=False)
    df.loc[idx[:15], "gender"] = "M"
    df.loc[idx[15:25], "gender"] = "f"
    df.loc[idx[25:], "gender"] = " male "
    df["smoker"] = df["smoker"].astype(object)
    s_idx = rng.choice(n, 30, replace=False)
    df.loc[s_idx[:12], "smoker"] = "yes"
    df.loc[s_idx[12:22], "smoker"] = "N"
    df.loc[s_idx[22:], "smoker"] = "Y"

    # Text mixed into a numeric column (inconsistent data types).
    df["age"] = df["age"].astype(object)
    df.loc[rng.choice(n, 3, replace=False), "age"] = "45 yrs"
    df.loc[rng.choice(n, 2, replace=False), "age"] = "unknown"

    # Impossible values.
    df["age"] = df["age"].astype(object)
    df.loc[rng.choice(n, 1), "age"] = -5
    df.loc[rng.choice(n, 1), "age"] = 150
    df.loc[rng.choice(n, 2, replace=False), "bmi"] = [0.0, 95.0]

    # Duplicate records.
    dupes = df.sample(8, random_state=1)
    df = pd.concat([df, dupes], ignore_index=True)
    return df.sample(frac=1, random_state=7).reset_index(drop=True)


def generate_dataset(n=N_PATIENTS, seed=SEED):
    """Build the full simulated dataset (clean data plus injected issues).

    Parameters
    ----------
    n : int
        Number of unique patients to simulate.
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    pandas.DataFrame
        Raw dataset with ``n + 8`` rows (8 duplicates).
    """
    rng = np.random.default_rng(seed)
    return _inject_quality_issues(_simulate_clean(n, rng), rng)


if __name__ == "__main__":
    data = generate_dataset()
    data.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved {len(data)} rows x {data.shape[1]} columns to {OUTPUT_PATH}")
