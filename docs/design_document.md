# Software Design Document

## 1. Problem statement, objectives and scope
**Problem.** Healthcare datasets are often messy (missing values, duplicates,
inconsistent labels), and analysts repeat the same cleaning and reporting
steps by hand. **Objective:** build a reproducible Python application that
accepts a patient dataset, cleans it, analyses it, produces charts and writes a
summary report. **Scope:** single-user, command-line tool; input CSV/JSON with
a fixed schema; descriptive statistics only. Out of scope: GUI, databases,
predictive modelling, real patient data.

## 2. Requirements
**Functional:** FR1 read CSV/JSON; FR2 validate required columns; FR3 handle
missing values, duplicates, inconsistent types/labels and invalid values; FR4
compute mean, median, std, min, max and frequency tables; FR5 generate >= 3
charts; FR6 save cleaned data, charts and report to an output folder; FR7
provide a command-line interface.
**Non-functional:** NFR1 reproducibility (fixed seeds, requirements.txt);
NFR2 maintainability (modules, PEP 8, docstrings); NFR3 reliability (error
handling, pytest tests); NFR4 usability (one command, clear messages);
NFR5 performance (processes 10^4 rows in seconds); NFR6 portability
(Windows/macOS/Linux, Python 3.9+); NFR7 privacy (synthetic data only).

## 3. SDLC stages applied
| Stage | What was done |
|---|---|
| Requirements | Analysed the brief; wrote FR/NFR list and dataset schema |
| Design | Chose modular layout (loader, preprocessing, analysis, visualisation, report, pipeline); drew workflow diagram |
| Implementation | Coded modules with docstrings and PEP 8 on feature branches; committed incrementally |
| Testing | 20 pytest tests: valid input, missing values, invalid data, end-to-end |
| Deployment | Packaged with requirements.txt, README, virtual-environment instructions and GitHub repository |

## 4. Architecture / workflow
See `docs/architecture.png`: CSV/JSON file -> data_loader -> preprocessing ->
analysis -> visualization -> report -> output folder; `pipeline.py` orchestrates
and `main.py` provides the CLI.

## 5. Technical specifications
Language Python 3.9+; libraries NumPy, pandas, Matplotlib, pytest, Jupyter;
input CSV/JSON with 15 columns (>= 200 rows); outputs `cleaned_dataset.csv`,
`summary_statistics.csv`, five PNG charts, `summary_report.md`; version control
Git/GitHub.
