import pandas as pd
import json

from schema_inference import infer_schema

from quality_scoring import (
    get_quality_metrics,
    compare_quality_scores
)

from imputation import (
    statistical_imputation,
    knn_imputation,
    regression_imputation,
    iterative_imputation
)

from normalization import normalize_dataset


def remove_duplicates(df):
    """
    Remove exact duplicate rows.
    """

    before = len(df)

    df = df.drop_duplicates().reset_index(drop=True)

    after = len(df)

    removed = before - after

    return df, removed


def apply_imputation(df, method="statistical"):
    """
    Apply the selected missing-value imputation method.
    """

    if method == "statistical":
        return statistical_imputation(df)

    elif method == "knn":
        return knn_imputation(df)

    elif method == "regression":
        return regression_imputation(df)

    elif method == "iterative":
        return iterative_imputation(df)

    else:
        raise ValueError(
            "Invalid imputation method. "
            "Choose statistical, knn, regression, or iterative."
        )


def clean_dataset(
    input_file,
    output_file,
    log_file,
    imputation_method="statistical"
):
    """
    Main automated data cleaning pipeline.
    """

    # 1. Load dataset
    original_df = pd.read_csv(input_file)

    df = original_df.copy()

    # 2. Quality before cleaning
    before_metrics = get_quality_metrics(df)
    before_score = before_metrics["quality_score"]

    # 3. Schema inference
    schema = infer_schema(df)

    # 4. Normalize data
    df = normalize_dataset(df)

    # 5. Missing-value imputation
    missing_before_imputation = int(
        df.isnull().sum().sum()
    )

    df = apply_imputation(
        df,
        method=imputation_method
    )

    missing_after_imputation = int(
        df.isnull().sum().sum()
    )

    values_imputed = (
        missing_before_imputation
        - missing_after_imputation
    )

    # 6. Remove exact duplicates
    df, duplicates_removed = remove_duplicates(df)

    # 7. Quality after cleaning
    after_metrics = get_quality_metrics(df)
    after_score = after_metrics["quality_score"]

    # 8. Compare quality
    quality_comparison = compare_quality_scores(
        before_score,
        after_score
    )

    # 9. Save cleaned dataset
    df.to_csv(
        output_file,
        index=False
    )

    # 10. Create detailed cleaning log
    cleaning_log = {

        "input_file": input_file,

        "output_file": output_file,

        "imputation_method": imputation_method,

        "original_rows": len(original_df),

        "cleaned_rows": len(df),

        "original_columns": len(original_df.columns),

        "cleaned_columns": len(df.columns),

        "missing_values_before": missing_before_imputation,

        "missing_values_after": missing_after_imputation,

        "values_imputed": values_imputed,

        "duplicates_removed": duplicates_removed,

        "quality_before": before_metrics,

        "quality_after": after_metrics,

        "quality_comparison": quality_comparison,

        "cleaning_operations": [
            "Schema inference",
            "String normalization",
            "Numeric type normalization",
            "Date normalization",
            "Categorical normalization",
            "Missing-value imputation",
            "Exact duplicate removal",
            "Data quality scoring"
        ],

        "schema": schema
    }

    # 11. Save cleaning log
    with open(
        log_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            cleaning_log,
            file,
            indent=4,
            default=str
        )

    return df, cleaning_log