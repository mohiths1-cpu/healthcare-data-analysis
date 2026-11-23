"""Data input: read a CSV or JSON file into a validated DataFrame."""
from pathlib import Path

import pandas as pd

from healthcare_analysis.config import NA_VALUES, REQUIRED_COLUMNS


def load_data(path):
    """Read a dataset from a CSV or JSON file.

    Parameters
    ----------
    path : str or pathlib.Path
        Location of a ``.csv`` or ``.json`` file.

    Returns
    -------
    pandas.DataFrame
        The raw, unmodified records.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    ValueError
        If the extension is unsupported, the file is empty or required
        columns are missing.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    suffix = path.suffix.lower()
    if suffix == ".csv":
        df = pd.read_csv(path, na_values=NA_VALUES, dtype=object)
    elif suffix == ".json":
        df = pd.read_json(path, dtype=False)
    else:
        raise ValueError(
            f"Unsupported file type '{suffix}'. Use .csv or .json")

    if df.empty:
        raise ValueError("The input file contains no records.")
    validate_columns(df)
    return df


def validate_columns(df, required=REQUIRED_COLUMNS):
    """Check that every required column is present.

    Parameters
    ----------
    df : pandas.DataFrame
        Table to check.
    required : list of str
        Column names that must exist.

    Raises
    ------
    ValueError
        If one or more required columns are absent.
    """
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")
