"""Project-wide constants: expected schema, valid ranges and label maps."""

REQUIRED_COLUMNS = [
    "patient_id", "age", "gender", "region", "bmi", "systolic_bp",
    "diastolic_bp", "glucose", "cholesterol", "smoker",
    "physical_activity", "visit_date", "hospital_stay_days",
    "diabetes", "hypertension",
]

NUMERIC_COLUMNS = [
    "age", "bmi", "systolic_bp", "diastolic_bp", "glucose", "cholesterol",
    "hospital_stay_days", "diabetes", "hypertension",
]

CATEGORICAL_COLUMNS = ["gender", "region", "smoker", "physical_activity"]

# Clinically plausible limits; values outside become missing and are imputed.
VALID_RANGES = {
    "age": (0, 110),
    "bmi": (10, 60),
    "systolic_bp": (70, 250),
    "diastolic_bp": (40, 150),
    "glucose": (40, 500),
    "cholesterol": (80, 500),
    "hospital_stay_days": (0, 60),
}

NA_VALUES = ["", "NA", "N/A", "na", "n/a", "null", "NULL", "unknown",
             "Unknown", "?"]

GENDER_MAP = {"m": "Male", "male": "Male", "f": "Female", "female": "Female"}
YES_NO_MAP = {"y": "Yes", "yes": "Yes", "n": "No", "no": "No"}

AGE_BINS = [0, 29, 44, 59, 74, 200]
AGE_LABELS = ["<30", "30-44", "45-59", "60-74", "75+"]
BMI_BINS = [0, 18.5, 25, 30, 100]
BMI_LABELS = ["Underweight", "Normal", "Overweight", "Obese"]
