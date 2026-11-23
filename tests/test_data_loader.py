"""Tests for data input (valid input, missing file, invalid data)."""
import pytest

from healthcare_analysis.data_loader import load_data, validate_columns


def test_load_valid_csv_has_required_columns():
    df = load_data("data/healthcare_patients.csv")
    assert len(df) >= 200
    validate_columns(df)  # raises if a column is missing


def test_load_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        load_data("does_not_exist.csv")


def test_load_unsupported_extension_raises(tmp_path):
    bad = tmp_path / "data.txt"
    bad.write_text("a,b\n1,2\n")
    with pytest.raises(ValueError):
        load_data(bad)


def test_load_csv_missing_columns_raises(tmp_path):
    bad = tmp_path / "short.csv"
    bad.write_text("patient_id,age\nP1,30\n")
    with pytest.raises(ValueError):
        load_data(bad)


def test_load_json_file(tmp_path, raw_df):
    path = tmp_path / "patients.json"
    raw_df.to_json(path, orient="records")
    assert len(load_data(path)) == len(raw_df)
