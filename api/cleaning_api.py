import os
import sys
import json

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

from cleaning import clean_dataset


def run_cleaning_api(
    input_file,
    output_file,
    log_file,
    imputation_method="statistical"
):
    """
    Cleaning API function.

    Input:
        Raw CSV dataset

    Output:
        Cleaned CSV dataset
        Cleaning log JSON
    """

    cleaned_df, cleaning_log = clean_dataset(
        input_file=input_file,
        output_file=output_file,
        log_file=log_file,
        imputation_method=imputation_method
    )

    return {
        "status": "success",
        "message": "Dataset cleaned successfully",
        "output_file": output_file,
        "log_file": log_file,
        "quality_comparison": cleaning_log[
            "quality_comparison"
        ],
        "rows_before": cleaning_log[
            "original_rows"
        ],
        "rows_after": cleaning_log[
            "cleaned_rows"
        ],
        "duplicates_removed": cleaning_log[
            "duplicates_removed"
        ],
        "values_imputed": cleaning_log[
            "values_imputed"
        ]
    }