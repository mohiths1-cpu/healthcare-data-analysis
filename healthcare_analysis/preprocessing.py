"""Data preprocessing: clean types, labels, duplicates, ranges and gaps."""
import numpy as np
import pandas as pd

from healthcare_analysis.config import (
    AGE_BINS, AGE_LABELS, BMI_BINS, BMI_LABELS, CATEGORICAL_COLUMNS,
    GENDER_MAP, NUMERIC_COLUMNS, VALID_RANGES, YES_NO_MAP,
)


def coerce_numeric(df, columns=NUMERIC_COLUMNS):
    """Convert columns to numbers, extracting digits from text like '45 yrs'.

    Parameters
    ----------
    df : pandas.DataFrame
        Input table (not modified).
    columns : list of str
        Columns that should be numeric.

    Returns
    -------
    pandas.DataFrame
        Copy in which unparseable entries are ``NaN``.
    """
    df = df.copy()
    for col in columns:
        if col in df.columns:
            extracted = (df[col].astype("string")
                         .str.extract(r"(-?\d+\.?\d*)", expand=False))
            numbers = pd.to_numeric(extracted, errors="coerce")
            df[col] = numbers.astype("float64")
    return df


def standardise_categories(df):
    """Unify inconsistent text labels (case, whitespace, abbreviations).

    Parameters
    ----------
    df : pandas.DataFrame
        Input table (not modified).

    Returns
    -------
    pandas.DataFrame
        Copy with ``gender`` as Male/Female, ``smoker`` as Yes/No and
        other categorical columns in title case. Unrecognised labels
        become ``NaN``.
    """
    df = df.copy()
    for col in CATEGORICAL_COLUMNS:
        df[col] = df[col].astype("string").str.strip()
    df["gender"] = df["gender"].str.lower().map(GENDER_MAP)
    df["smoker"] = df["smoker"].str.lower().map(YES_NO_MAP)
    df["region"] = df["region"].str.title()
    df["physical_activity"] = df["physical_activity"].str.title()
    for col in CATEGORICAL_COLUMNS:
        df[col] = df[col].astype(object).where(df[col].notna(), np.nan)
    return df


def remove_duplicates(df, subset="patient_id"):
    """Drop repeated patient records, keeping the first occurrence.

    Parameters
    ----------
    df : pandas.DataFrame
        Input table.
    subset : str or list of str
        Column(s) identifying a unique record.

    Returns
    -------
    tuple of (pandas.DataFrame, int)
        Table without duplicates and the number of rows removed.
    """
    cleaned = df.drop_duplicates(subset=subset, keep="first")
    return cleaned.reset_index(drop=True), len(df) - len(cleaned)


def flag_invalid_values(df, ranges=VALID_RANGES):
    """Replace values outside plausible ranges with ``NaN``.

    Parameters
    ----------
    df : pandas.DataFrame
        Table with numeric columns.
    ranges : dict
        Mapping ``column -> (minimum, maximum)``.

    Returns
    -------
    tuple of (pandas.DataFrame, dict)
        Cleaned copy and a dict with the count of invalid values per column.
    """
    df = df.copy()
    counts = {}
    for col, (low, high) in ranges.items():
        if col not in df.columns:
            continue
        bad = df[col].notna() & ~df[col].between(low, high)
        counts[col] = int(bad.sum())
        df.loc[bad, col] = np.nan
    return df, counts


def handle_missing(df):
    """Impute gaps: median for numeric columns, mode for categorical ones.

    Parameters
    ----------
    df : pandas.DataFrame
        Table that may contain ``NaN`` values.

    Returns
    -------
    tuple of (pandas.DataFrame, dict)
        Imputed copy and a dict with the number of values filled per column.
    """
    df = df.copy()
    filled = {}
    for col in df.columns:
        n_missing = int(df[col].isna().sum())
        if n_missing == 0:
            continue
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].median())
        elif col in CATEGORICAL_COLUMNS:
            df[col] = df[col].fillna(df[col].mode().iloc[0])
        else:
            continue
        filled[col] = n_missing
    return df, filled


def add_derived_features(df):
    """Add ``age_group`` and ``bmi_category`` columns.

    Parameters
    ----------
    df : pandas.DataFrame
        Table with ``age`` and ``bmi`` columns.

    Returns
    -------
    pandas.DataFrame
        Copy with the two new categorical columns.
    """
    df = df.copy()
    df["age_group"] = pd.cut(df["age"], bins=AGE_BINS, labels=AGE_LABELS)
    df["bmi_category"] = pd.cut(df["bmi"], bins=BMI_BINS, labels=BMI_LABELS,
                                right=False)
    return df


def preprocess(df):
    """Run the full cleaning pipeline.

    Order: type coercion, label standardisation, de-duplication, range
    validation, imputation, derived features.

    Parameters
    ----------
    df : pandas.DataFrame
        Raw table from :func:`data_loader.load_data`.

    Returns
    -------
    tuple of (pandas.DataFrame, dict)
        Clean table and a summary dict describing every change made.
    """
    summary = {"rows_raw": len(df)}
    df = coerce_numeric(df)
    df = standardise_categories(df)
    df["visit_date"] = pd.to_datetime(df["visit_date"], errors="coerce")
    summary["missing_before"] = {
        c: int(n) for c, n in df.isna().sum().items() if n > 0}

    df, summary["duplicates_removed"] = remove_duplicates(df)
    df, summary["invalid_values"] = flag_invalid_values(df)
    df, summary["values_imputed"] = handle_missing(df)

    for col in ["age", "systolic_bp", "diastolic_bp", "hospital_stay_days",
                "diabetes", "hypertension"]:
        df[col] = df[col].round().astype(int)
    df = add_derived_features(df)
    summary["rows_clean"] = len(df)
    return df, summary
