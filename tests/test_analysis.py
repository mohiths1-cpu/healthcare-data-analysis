"""Tests for analysis and visualisation functions."""
import pytest

from healthcare_analysis.analysis import (
    frequency_distribution, prevalence_by_group, summary_statistics)
from healthcare_analysis.visualization import generate_all_charts


def test_summary_statistics_known_values(numeric_df):
    stats = summary_statistics(numeric_df, ["age"])
    assert stats.loc["age", "mean"] == 30
    assert stats.loc["age", "median"] == 30
    assert stats.loc["age", "min"] == 10
    assert stats.loc["age", "max"] == 50
    assert stats.loc["age", "std"] == pytest.approx(15.81, abs=0.01)


def test_summary_statistics_ignores_missing(numeric_df):
    stats = summary_statistics(numeric_df, ["bmi"])
    assert stats.loc["bmi", "count"] == 4
    assert stats.loc["bmi", "mean"] == 23.0


def test_frequency_distribution_percentages(clean_df):
    freq = frequency_distribution(clean_df, "gender")
    assert freq["count"].sum() == len(clean_df)
    assert freq["percent"].sum() == pytest.approx(100, abs=0.2)


def test_frequency_distribution_unknown_column_raises(clean_df):
    with pytest.raises(KeyError):
        frequency_distribution(clean_df, "not_a_column")


def test_prevalence_by_group_range(clean_df):
    prevalence = prevalence_by_group(clean_df, "age_group", "diabetes")
    assert prevalence.between(0, 100).all()


def test_generate_all_charts_creates_png_files(clean_df, tmp_path):
    paths = generate_all_charts(clean_df, tmp_path)
    assert len(paths) >= 3
    assert all(p.exists() and p.stat().st_size > 0 for p in paths)
