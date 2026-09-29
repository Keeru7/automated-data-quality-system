import pandas as pd
import json


# 1. Check for missing values
def check_missing_values(df):

    results = {}

    for column in df.columns:

        missing_count = int(
            df[column].isnull().sum()
        )

        results[column] = {
            "missing_values": missing_count,
            "status": "PASS"
            if missing_count == 0
            else "FAIL"
        }

    return results


# 2. Check for duplicate rows
def check_duplicates(df):

    duplicate_count = int(
        df.duplicated().sum()
    )

    return {
        "duplicate_rows": duplicate_count,
        "status": "PASS"
        if duplicate_count == 0
        else "FAIL"
    }


# 3. Check data types
def check_data_types(df):

    results = {}

    for column in df.columns:

        results[column] = {
            "data_type": str(
                df[column].dtype
            ),
            "status": "PASS"
        }

    return results


# 4. Check numeric values
def check_numeric_values(df):

    results = {}

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    for column in numeric_columns:

        negative_count = int(
            (df[column] < 0).sum()
        )

        results[column] = {
            "negative_values": negative_count,
            "status": "PASS"
            if negative_count == 0
            else "CHECK"
        }

    return results


# 5. Check value ranges
def check_value_ranges(df):

    results = {}

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    for column in numeric_columns:

        minimum = df[column].min()
        maximum = df[column].max()

        results[column] = {
            "minimum": float(minimum),
            "maximum": float(maximum),
            "status": "PASS"
        }

    return results


# 6. Run all validation checks
def validate_dataset(input_file, output_file):

    # Read cleaned dataset
    df = pd.read_csv(input_file)

    # Run validation checks
    missing_results = check_missing_values(df)

    duplicate_results = check_duplicates(df)

    type_results = check_data_types(df)

    numeric_results = check_numeric_values(df)

    range_results = check_value_ranges(df)

    # Determine overall status
    all_passed = True

    # Check missing values
    for column in missing_results:

        if missing_results[column]["status"] == "FAIL":

            all_passed = False

    # Check duplicates
    if duplicate_results["status"] == "FAIL":

        all_passed = False

    # Check negative numeric values
    for column in numeric_results:

        if numeric_results[column]["status"] == "CHECK":

            all_passed = False

    if all_passed:

        final_status = "PASS"

    else:

        final_status = "CHECK"

    # Create final validation report
    validation_report = {

        "dataset": input_file,

        "overall_status": final_status,

        "missing_value_check": missing_results,

        "duplicate_check": duplicate_results,

        "data_type_check": type_results,

        "numeric_value_check": numeric_results,

        "value_range_check": range_results
    }

    # Save validation report
    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            validation_report,
            file,
            indent=4
        )

    return validation_report