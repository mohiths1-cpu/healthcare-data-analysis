"""Shared pytest fixtures."""
import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def raw_df():
    """Small raw table with typical quality problems."""
    return pd.DataFrame({
        "patient_id": ["P1", "P2", "P3", "P3", "P4", "P5"],
        "age": ["45", "52 yrs", "-5", "-5", None, "61"],
        "gender": ["M", " female ", "Male", "Male", "f", "MALE"],
        "region": ["north", "South", "East", "East", None, "West"],
        "bmi": ["25.1", "31.0", "0", "0", "28.4", None],
        "systolic_bp": ["120", "150", "130", "130", "140", "135"],
        "diastolic_bp": ["80", "95", "85", "85", "90", "88"],
        "glucose": ["90", "140", "100", "100", None, "110"],
        "cholesterol": ["180", "220", "200", "200", "210", "190"],
        "smoker": ["yes", "N", "Y", "Y", "no", None],
        "physical_activity": ["Low", "high", "Moderate", "Moderate",
                              "Low", "Low"],
        "visit_date": ["2024-01-05"] * 6,
        "hospital_stay_days": ["1", "3", "2", "2", "4", "0"],
        "diabetes": ["0", "1", "0", "0", "1", "0"],
        "hypertension": ["0", "1", "0", "0", "1", "0"],
    })


@pytest.fixture
def clean_df(raw_df):
    """Result of running the full preprocessing pipeline on ``raw_df``."""
    from healthcare_analysis.preprocessing import preprocess
    cleaned, _ = preprocess(raw_df)
    return cleaned


@pytest.fixture
def numeric_df():
    """Tiny table with known values for exact statistic checks."""
    return pd.DataFrame({"age": [10, 20, 30, 40, 50],
                         "bmi": [20.0, 22.0, 24.0, 26.0, np.nan]})
