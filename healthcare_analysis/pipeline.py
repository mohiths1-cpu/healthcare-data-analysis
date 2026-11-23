"""End-to-end pipeline: load, preprocess, analyse, visualise, report."""
from pathlib import Path

from healthcare_analysis.analysis import summary_statistics
from healthcare_analysis.data_loader import load_data
from healthcare_analysis.preprocessing import preprocess
from healthcare_analysis.report import build_report, save_report
from healthcare_analysis.visualization import generate_all_charts


def run_pipeline(input_path, output_dir="outputs"):
    """Execute the complete analysis and save every output.

    Parameters
    ----------
    input_path : str or pathlib.Path
        CSV or JSON dataset.
    output_dir : str or pathlib.Path
        Folder for the cleaned data, charts, statistics and report.

    Returns
    -------
    dict
        Paths of generated files and the cleaning summary.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    raw = load_data(input_path)
    clean, summary = preprocess(raw)

    clean_path = output_dir / "cleaned_dataset.csv"
    clean.to_csv(clean_path, index=False)

    stats_path = output_dir / "summary_statistics.csv"
    summary_statistics(clean).to_csv(stats_path)

    charts = generate_all_charts(clean, output_dir / "figures")
    report_path = save_report(build_report(clean, summary), output_dir)

    return {"cleaned_data": clean_path, "statistics": stats_path,
            "charts": charts, "report": report_path, "summary": summary}
