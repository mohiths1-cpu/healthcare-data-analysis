"""Summary report generation (Markdown)."""
from pathlib import Path

from healthcare_analysis.analysis import (
    frequency_distribution, key_findings, summary_statistics)


def build_report(df, cleaning_summary):
    """Compose a Markdown summary report.

    Parameters
    ----------
    df : pandas.DataFrame
        Clean table.
    cleaning_summary : dict
        Summary returned by :func:`preprocessing.preprocess`.

    Returns
    -------
    str
        Report text in Markdown.
    """
    lines = ["# Healthcare Data Analysis Report", "",
             "## 1. Data cleaning summary", "",
             f"- Raw records: {cleaning_summary['rows_raw']}",
             f"- Duplicates removed: {cleaning_summary['duplicates_removed']}",
             f"- Invalid values set to missing: "
             f"{sum(cleaning_summary['invalid_values'].values())}",
             f"- Missing values imputed: "
             f"{sum(cleaning_summary['values_imputed'].values())}",
             f"- Clean records: {cleaning_summary['rows_clean']}", "",
             "## 2. Key findings", ""]
    lines += [f"- {text}" for text in key_findings(df)]
    lines += ["", "## 3. Summary statistics", "",
              "```", summary_statistics(df).to_string(), "```", ""]
    for col in ["gender", "smoker", "physical_activity", "region"]:
        lines += [f"## Frequency: {col}", "",
                  "```", frequency_distribution(df, col).to_string(), "```",
                  ""]
    return "\n".join(lines)



def save_report(text, output_dir, filename="summary_report.md"):
    """Write the report text to disk.

    Parameters
    ----------
    text : str
        Report content.
    output_dir : str or pathlib.Path
        Destination folder (created if needed).
    filename : str
        Output file name.

    Returns
    -------
    pathlib.Path
        Path of the written file.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / filename
    path.write_text(text, encoding="utf-8")
    return path
