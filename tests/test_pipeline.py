"""End-to-end tests for the pipeline and command-line interface."""
import pandas as pd

from main import main
from healthcare_analysis.pipeline import run_pipeline


def test_pipeline_creates_all_outputs(tmp_path):
    result = run_pipeline("data/healthcare_patients.csv", tmp_path)
    assert result["cleaned_data"].exists()
    assert result["report"].exists()
    assert len(result["charts"]) >= 3
    cleaned = pd.read_csv(result["cleaned_data"])
    assert len(cleaned) >= 200
    assert cleaned.isna().sum().sum() == 0
    assert cleaned["patient_id"].is_unique


def test_cli_returns_error_code_for_bad_input(tmp_path):
    assert main(["--input", "nope.csv", "--output", str(tmp_path)]) == 1


def test_cli_success(tmp_path):
    code = main(["--input", "data/healthcare_patients.csv",
                 "--output", str(tmp_path)])
    assert code == 0
