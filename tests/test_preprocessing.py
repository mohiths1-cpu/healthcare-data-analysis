"""Tests for preprocessing (missing values, duplicates, invalid data)."""
import numpy as np
import pandas as pd

from healthcare_analysis.preprocessing import (
    coerce_numeric, flag_invalid_values, handle_missing,
    preprocess, remove_duplicates, standardise_categories)


def test_coerce_numeric_extracts_digits_from_text():
    df = pd.DataFrame({"age": ["45", "52 yrs", "abc", None]})
    out = coerce_numeric(df, ["age"])
    assert out["age"].iloc[0] == 45
    assert out["age"].iloc[1] == 52
    assert np.isnan(out["age"].iloc[2])


def test_standardise_categories_unifies_labels(raw_df):
    out = standardise_categories(raw_df)
    assert set(out["gender"].dropna()) == {"Male", "Female"}
    assert set(out["smoker"].dropna()) == {"Yes", "No"}
    assert out["region"].iloc[0] == "North"


def test_remove_duplicates_counts_removed_rows(raw_df):
    out, removed = remove_duplicates(raw_df)
    assert removed == 1
    assert out["patient_id"].is_unique


def test_flag_invalid_values_sets_nan():
    df = pd.DataFrame({"age": [30.0, -5.0, 150.0], "bmi": [22.0, 0.0, 25.0]})
    out, counts = flag_invalid_values(df, {"age": (0, 110), "bmi": (10, 60)})
    assert counts == {"age": 2, "bmi": 1}
    assert out["age"].isna().sum() == 2


def test_handle_missing_uses_median_and_mode():
    df = pd.DataFrame({"bmi": [20.0, 30.0, np.nan, 40.0],
                       "smoker": ["Yes", "Yes", "No", None]})
    out, filled = handle_missing(df)
    assert out["bmi"].iloc[2] == 30.0          # median of 20, 30, 40
    assert out["smoker"].iloc[3] == "Yes"      # most frequent value
    assert filled == {"bmi": 1, "smoker": 1}


def test_preprocess_leaves_no_missing_values(raw_df):
    clean, summary = preprocess(raw_df)
    assert clean.isna().sum().sum() == 0
    assert summary["duplicates_removed"] == 1
    assert summary["rows_clean"] == 5
    assert "age_group" in clean.columns
