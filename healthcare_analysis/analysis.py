"""Data analysis: summary statistics, frequencies and group comparisons."""
import numpy as np
import pandas as pd

DEFAULT_STAT_COLUMNS = ["age", "bmi", "systolic_bp", "diastolic_bp",
                        "glucose", "cholesterol", "hospital_stay_days"]


def summary_statistics(df, columns=None):
    """Compute descriptive statistics for numeric columns.

    Parameters
    ----------
    df : pandas.DataFrame
        Clean table.
    columns : list of str, optional
        Columns to summarise (defaults to the main clinical measures).

    Returns
    -------
    pandas.DataFrame
        One row per column with count, mean, median, std, min, max, Q1, Q3.
    """
    columns = columns or DEFAULT_STAT_COLUMNS
    rows = {}
    for col in columns:
        values = df[col].to_numpy(dtype=float)
        values = values[~np.isnan(values)]
        if values.size == 0:
            raise ValueError(f"Column '{col}' has no valid values.")
        rows[col] = {
            "count": values.size,
            "mean": values.mean(),
            "median": np.median(values),
            "std": values.std(ddof=1) if values.size > 1 else 0.0,
            "min": values.min(),
            "max": values.max(),
            "q1": np.percentile(values, 25),
            "q3": np.percentile(values, 75),
        }
    return pd.DataFrame(rows).T.round(2)


def frequency_distribution(df, column):
    """Count and percentage of each category in a column.

    Parameters
    ----------
    df : pandas.DataFrame
        Clean table.
    column : str
        Categorical column name.

    Returns
    -------
    pandas.DataFrame
        Columns ``count`` and ``percent`` indexed by category.
    """
    if column not in df.columns:
        raise KeyError(f"Column '{column}' not found.")
    counts = df[column].value_counts()
    percent = (counts / counts.sum() * 100).round(1)
    return pd.DataFrame({"count": counts, "percent": percent})


def prevalence_by_group(df, group_col, outcome_col):
    """Percentage of patients with a condition within each group.

    Parameters
    ----------
    df : pandas.DataFrame
        Clean table.
    group_col : str
        Grouping column (e.g. ``age_group``).
    outcome_col : str
        Binary 0/1 column (e.g. ``diabetes``).

    Returns
    -------
    pandas.Series
        Prevalence in percent per group.
    """
    return (df.groupby(group_col, observed=True)[outcome_col]
            .mean().mul(100).round(1))


def correlation_matrix(df, columns=None):
    """Pearson correlation between numeric columns.

    Parameters
    ----------
    df : pandas.DataFrame
        Clean table.
    columns : list of str, optional
        Columns to correlate.

    Returns
    -------
    pandas.DataFrame
        Square correlation matrix rounded to 2 decimals.
    """
    columns = columns or DEFAULT_STAT_COLUMNS + ["diabetes", "hypertension"]
    return df[columns].corr().round(2)


def group_comparison(df, group_col, value_col):
    """Mean, median and count of a measure for each group.

    Parameters
    ----------
    df : pandas.DataFrame
        Clean table.
    group_col : str
        Grouping column.
    value_col : str
        Numeric column to summarise.

    Returns
    -------
    pandas.DataFrame
        Aggregated statistics per group.
    """
    return (df.groupby(group_col, observed=True)[value_col]
            .agg(["count", "mean", "median"]).round(2))


def key_findings(df):
    """Generate plain-language findings from the data.

    Parameters
    ----------
    df : pandas.DataFrame
        Clean table.

    Returns
    -------
    list of str
        Short sentences describing the main results.
    """
    corr = df["bmi"].corr(df["systolic_bp"])
    age_prev = prevalence_by_group(df, "age_group", "diabetes")
    smoker_bp = df.groupby("smoker")["systolic_bp"].mean().round(1)
    return [
        f"{len(df)} patients analysed; mean age {df['age'].mean():.1f} years.",
        f"Diabetes prevalence: {df['diabetes'].mean() * 100:.1f}%; "
        f"hypertension prevalence: {df['hypertension'].mean() * 100:.1f}%.",
        f"Diabetes prevalence is highest in the {age_prev.idxmax()} age "
        f"group ({age_prev.max():.1f}%).",
        f"BMI and systolic BP are positively correlated (r = {corr:.2f}).",
        f"Mean systolic BP: smokers {smoker_bp.get('Yes', float('nan'))} "
        f"vs non-smokers {smoker_bp.get('No', float('nan'))} mmHg.",
    ]
