import pandas as pd
import json
import sys
import os


# Add src folder to Python path
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "src"
        )
    )
)


from profiling import (
    detect_semantic_meaning,
    detect_mixed_type,
    check_type_consistency,
    check_format_consistency,
    detect_pii,
    detect_suspicious_column
)


def generate_profile(input_file, output_file):

    # Read CSV file
    df = pd.read_csv(input_file)

    # Identify column types
    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include="object"
    ).columns.tolist()

    # Dataset information
    dataset_summary = {
        "file_name": os.path.basename(input_file),
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "numeric_columns": numeric_columns,
        "categorical_columns": categorical_columns
    }

    column_profiles = []

    # Analyze every column
    for column in df.columns:

        series = df[column]

        missing_count = int(
            series.isnull().sum()
        )

        missing_percentage = round(
            (missing_count / len(df)) * 100,
            2
        )

        unique_count = int(
            series.nunique()
        )

        semantic_meaning = detect_semantic_meaning(
            column
        )

        mixed_type = detect_mixed_type(
            series
        )

        type_consistency = check_type_consistency(
            series
        )

        format_consistency = check_format_consistency(
            column,
            series
        )

        potential_pii, pii_reason = detect_pii(
            column,
            series
        )

        suspicious, suspicious_reason = (
            detect_suspicious_column(
                column,
                series
            )
        )

        column_profiles.append({

            "column_name": column,

            "data_type": str(
                series.dtype
            ),

            "semantic_meaning": semantic_meaning,

            "missing_values": missing_count,

            "missing_percentage": missing_percentage,

            "unique_values": unique_count,

            "mixed_type": mixed_type,

            "type_consistency": type_consistency,

            "format_consistency": format_consistency,

            "potential_pii": potential_pii,

            "pii_reason": pii_reason,

            "suspicious": suspicious,

            "suspicious_reason": suspicious_reason
        })

    # Create final report
    final_report = {

        "dataset_summary": dataset_summary,

        "column_profiles": column_profiles
    }

    # Save JSON report
    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            final_report,
            file,
            indent=4
        )

    return final_report