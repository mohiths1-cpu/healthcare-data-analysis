# Healthcare Data Analysis and Reporting System

A modular Python application that loads a patient dataset, cleans it, computes
summary statistics, draws charts and writes a summary report. Built for the
course *Software Development for Data Science* (Assignment 2).

## Objectives
- Apply the software development life cycle to a small data-science tool.
- Clean messy healthcare data reproducibly (missing values, duplicates,
  inconsistent labels, impossible values).
- Produce statistics, at least three Matplotlib charts and a text report.
- Show good engineering practice: modules, PEP 8, pytest tests, Git, docs.

## Features
- Reads **CSV or JSON** input with schema validation and clear errors.
- Cleaning: type coercion, label standardisation, duplicate removal,
  range validation, median/mode imputation, derived `age_group`/`bmi_category`.
- Statistics: mean, median, std, min, max, quartiles, frequency tables,
  prevalence by group, correlation matrix.
- Five charts (histogram, grouped bar, box plot, scatter + trend, heatmap).
- Outputs: cleaned CSV, statistics CSV, PNG charts, Markdown report.
- 20 automated pytest tests.

## Project structure
```
healthcare-data-analysis/
├── main.py                    # command-line entry point
├── healthcare_analysis/       # application package
│   ├── config.py              # schema, valid ranges, label maps
│   ├── data_loader.py         # CSV/JSON input + validation
│   ├── preprocessing.py       # cleaning functions
│   ├── analysis.py            # statistics and findings
│   ├── visualization.py       # Matplotlib charts
│   ├── report.py              # Markdown report
│   └── pipeline.py            # ties the steps together
├── data/
│   ├── generate_dataset.py    # reproducible simulated dataset (seed 42)
│   └── healthcare_patients.csv
├── tests/                     # pytest unit + end-to-end tests
├── notebooks/healthcare_analysis.ipynb
├── docs/                      # design document, data ethics, figures
├── outputs/                   # generated results
├── requirements.txt
└── pytest.ini
```

## Installation
Requires Python 3.9 or newer.

```bash
git clone <your-repository-url>
cd healthcare-data-analysis

# create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows (cmd / PowerShell)

pip install -r requirements.txt
```

## Running the application
```bash
python main.py                                  # uses data/healthcare_patients.csv
python main.py --input my_data.json --output results
```
Results appear in `outputs/` (or the folder given with `--output`):
`cleaned_dataset.csv`, `summary_statistics.csv`, `summary_report.md` and
`figures/*.png`.

## Reproducing the results
The dataset is simulated and fully reproducible:
```bash
python data/generate_dataset.py     # recreates data/healthcare_patients.csv (seed 42)
python main.py                      # regenerates every output
pytest -v                           # runs the 20 tests
jupyter notebook notebooks/healthcare_analysis.ipynb
```
Fixed random seeds guarantee identical data and results on every run.

## Dataset
Simulated records for 300 patients (308 raw rows including 8 deliberate
duplicates) and 15 attributes: `patient_id, age, gender, region, bmi,
systolic_bp, diastolic_bp, glucose, cholesterol, smoker, physical_activity,
visit_date, hospital_stay_days, diabetes, hypertension`. Data-quality
problems were injected on purpose so the cleaning code has real work to do.
The data are **synthetic**; the generator script is the source.

## Data ethics
- **Privacy:** no real individuals; IDs are fake. With real data, remove or
  pseudonymise direct identifiers and follow rules such as HIPAA/GDPR or
  India's DPDP Act 2023.
- **Licensing:** dataset and code are original work for educational use
  (MIT-style licence for the code). If you swap in a public dataset, credit
  its source and respect its licence.
- **Responsible use:** simulated results must not inform clinical decisions;
  imputation and small groups limit reliability; correlation is not causation.
  See `docs/data_ethics.md`.

## Limitations and future work
The application uses simple imputation and descriptive statistics only.
Future work: model-based imputation, hypothesis tests, a web dashboard.
