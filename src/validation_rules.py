import pandas as pd
import re


def create_validation_result(
    column,
    rule,
    status,
    severity,
    message
):
    """
    Create a standard validation result.
    """

    return {
        "column": column,
        "rule": rule,
        "status": status,
        "severity": severity,
        "message": message
    }


def validate_dataset_structure(df):
    """
    Validate basic dataset structure.
    """

    results = []

    if df.empty:

        results.append(
            create_validation_result(
                column="dataset",
                rule="dataset_not_empty",
                status="failed",
                severity="high",
                message="Dataset is empty."
            )
        )

    else:

        results.append(
            create_validation_result(
                column="dataset",
                rule="dataset_not_empty",
                status="passed",
                severity="none",
                message="Dataset contains records."
            )
        )

    return results


def validate_missing_values(df):
    """
    Detect remaining missing values.
    """

    results = []

    for column in df.columns:

        missing_count = int(
            df[column].isnull().sum()
        )

        if missing_count > 0:

            missing_percentage = (
                missing_count / len(df)
            ) * 100

            if missing_percentage >= 20:
                severity = "high"

            elif missing_percentage >= 5:
                severity = "medium"

            else:
                severity = "low"

            results.append(
                create_validation_result(
                    column=column,
                    rule="missing_values",
                    status="failed",
                    severity=severity,
                    message=(
                        f"{missing_count} missing values "
                        f"({missing_percentage:.2f}%)."
                    )
                )
            )

        else:

            results.append(
                create_validation_result(
                    column=column,
                    rule="missing_values",
                    status="passed",
                    severity="none",
                    message="No missing values detected."
                )
            )

    return results


def validate_email_column(df, column):
    """
    Validate email addresses.
    """

    results = []

    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    for index, value in df[column].items():

        if pd.isna(value):
            continue

        value = str(value).strip()

        if re.match(email_pattern, value):

            results.append(
                create_validation_result(
                    column=column,
                    rule="email_format",
                    status="passed",
                    severity="none",
                    message=f"Valid email format at row {index}."
                )
            )

        else:

            results.append(
                create_validation_result(
                    column=column,
                    rule="email_format",
                    status="failed",
                    severity="high",
                    message=f"Invalid email format at row {index}."
                )
            )

    return results


def validate_phone_column(df, column):
    """
    Validate phone numbers.
    """

    results = []

    for index, value in df[column].items():

        if pd.isna(value):
            continue

        value = str(value).strip()

        digits = re.sub(r"\D", "", value)

        if 10 <= len(digits) <= 15:

            results.append(
                create_validation_result(
                    column=column,
                    rule="phone_format",
                    status="passed",
                    severity="none",
                    message=f"Valid phone format at row {index}."
                )
            )

        else:

            results.append(
                create_validation_result(
                    column=column,
                    rule="phone_format",
                    status="failed",
                    severity="high",
                    message=f"Invalid phone format at row {index}."
                )
            )

    return results


def validate_postcode_column(df, column):
    """
    Validate postcode values.
    """

    results = []

    for index, value in df[column].items():

        if pd.isna(value):
            continue

        value = str(value).strip()

        if re.match(r"^\d{5,6}$", value):

            results.append(
                create_validation_result(
                    column=column,
                    rule="postcode_format",
                    status="passed",
                    severity="none",
                    message=f"Valid postcode at row {index}."
                )
            )

        else:

            results.append(
                create_validation_result(
                    column=column,
                    rule="postcode_format",
                    status="failed",
                    severity="medium",
                    message=f"Invalid postcode at row {index}."
                )
            )

    return results


def validate_numeric_range(
    df,
    column,
    minimum=None,
    maximum=None
):
    """
    Validate whether numeric values
    fall within an expected range.
    """

    results = []

    if column not in df.columns:
        return results

    numeric_values = pd.to_numeric(
        df[column],
        errors="coerce"
    )

    for index, value in numeric_values.items():

        if pd.isna(value):
            continue

        invalid = False

        if minimum is not None and value < minimum:
            invalid = True

        if maximum is not None and value > maximum:
            invalid = True

        if invalid:

            results.append(
                create_validation_result(
                    column=column,
                    rule="numeric_range",
                    status="failed",
                    severity="high",
                    message=(
                        f"Value {value} at row {index} "
                        f"is outside the expected range."
                    )
                )
            )

        else:

            results.append(
                create_validation_result(
                    column=column,
                    rule="numeric_range",
                    status="passed",
                    severity="none",
                    message=(
                        f"Value {value} at row {index} "
                        f"is within the expected range."
                    )
                )
            )

    return results
def validate_categorical_consistency(
    df,
    column,
    allowed_values
):
    """
    Validate whether categorical values
    belong to the allowed set.
    """

    results = []

    if column not in df.columns:
        return results

    for index, value in df[column].items():

        if pd.isna(value):
            continue

        value = str(value).strip()

        if value in allowed_values:

            results.append(
                create_validation_result(
                    column=column,
                    rule="categorical_consistency",
                    status="passed",
                    severity="none",
                    message=(
                        f"Value '{value}' at row {index} "
                        f"is an allowed category."
                    )
                )
            )

        else:

            results.append(
                create_validation_result(
                    column=column,
                    rule="categorical_consistency",
                    status="failed",
                    severity="medium",
                    message=(
                        f"Unexpected category '{value}' "
                        f"at row {index}."
                    )
                )
            )

    return results