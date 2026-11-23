"""Command-line entry point for the healthcare analysis application."""
import argparse
import logging
import sys

from healthcare_analysis.pipeline import run_pipeline

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def parse_args(argv=None):
    """Parse command-line arguments.

    Parameters
    ----------
    argv : list of str, optional
        Arguments (defaults to ``sys.argv[1:]``).

    Returns
    -------
    argparse.Namespace
    """
    parser = argparse.ArgumentParser(
        description="Healthcare data analysis and reporting system")
    parser.add_argument("--input", default="data/healthcare_patients.csv",
                        help="CSV or JSON dataset (default: %(default)s)")
    parser.add_argument("--output", default="outputs",
                        help="Output directory (default: %(default)s)")
    return parser.parse_args(argv)


def main(argv=None):
    """Run the pipeline and print a short summary.

    Parameters
    ----------
    argv : list of str, optional
        Command-line arguments.

    Returns
    -------
    int
        Exit code (0 = success, 1 = error).
    """
    args = parse_args(argv)
    try:
        result = run_pipeline(args.input, args.output)
    except (FileNotFoundError, ValueError) as error:
        logging.error("%s", error)
        return 1
    summary = result["summary"]
    logging.info("Rows: %d raw -> %d clean (%d duplicates removed)",
                 summary["rows_raw"], summary["rows_clean"],
                 summary["duplicates_removed"])
    logging.info("Saved cleaned data, %d charts and report to '%s'",
                 len(result["charts"]), args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
