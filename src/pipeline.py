import os
import sys


# Add project folders to Python path
BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

SRC_DIR = os.path.join(
    BASE_DIR,
    "src"
)

API_DIR = os.path.join(
    BASE_DIR,
    "api"
)

sys.path.append(SRC_DIR)
sys.path.append(API_DIR)


# Import project modules
from profiling_api import generate_profile
from cleaning import clean_dataset
from validation import validate_dataset


def run_pipeline(input_file):

    # Project folders
    data_folder = os.path.join(
        BASE_DIR,
        "data"
    )

    reports_folder = os.path.join(
        BASE_DIR,
        "reports"
    )

    # Create folders if they don't exist
    os.makedirs(
        data_folder,
        exist_ok=True
    )

    os.makedirs(
        reports_folder,
        exist_ok=True
    )

    # Output files
    cleaned_file = os.path.join(
        data_folder,
        "cleaned_data.csv"
    )

    profiling_report = os.path.join(
        reports_folder,
        "pipeline_profiling_report.json"
    )

    cleaning_report = os.path.join(
        reports_folder,
        "pipeline_cleaning_report.json"
    )

    validation_report = os.path.join(
        reports_folder,
        "pipeline_validation_report.json"
    )

    # -----------------------------
    # STEP 1: PROFILE
    # -----------------------------

    print("Step 1: Profiling dataset...")

    profile_result = generate_profile(
        input_file,
        profiling_report
    )

    print("Profiling completed.")


    # -----------------------------
    # STEP 2: CLEAN
    # -----------------------------

    print("Step 2: Cleaning dataset...")

    cleaned_df, clean_result = clean_dataset(
        input_file,
        cleaned_file,
        cleaning_report
    )

    print("Cleaning completed.")


    # -----------------------------
    # STEP 3: VALIDATE
    # -----------------------------

    print("Step 3: Validating dataset...")

    validation_result = validate_dataset(
        cleaned_file,
        validation_report
    )

    print("Validation completed.")


    # -----------------------------
    # FINAL RESULT
    # -----------------------------

    print("\nPipeline completed successfully.")

    print(
        "Validation Status:",
        validation_result["overall_status"]
    )

    return {
        "profiling": profile_result,
        "cleaning": clean_result,
        "validation": validation_result
    }