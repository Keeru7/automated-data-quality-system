import pandas as pd
import numpy as np


def calculate_numeric_drift(
    reference_series,
    current_series
):
    """
    Calculate distribution drift for a numeric column
    using the difference between means and standard deviations.
    """

    reference = pd.to_numeric(
        reference_series,
        errors="coerce"
    ).dropna()

    current = pd.to_numeric(
        current_series,
        errors="coerce"
    ).dropna()

    if len(reference) == 0 or len(current) == 0:
        return {
            "status": "failed",
            "drift_score": 0,
            "message": "Not enough numeric data."
        }

    reference_mean = reference.mean()
    current_mean = current.mean()

    reference_std = reference.std()

    if reference_std == 0:
        if current_mean == reference_mean:
            drift_score = 0
        else:
            drift_score = 1
    else:
        drift_score = abs(
            current_mean - reference_mean
        ) / reference_std

    if drift_score >= 1:
        status = "drift_detected"
        severity = "high"

    elif drift_score >= 0.5:
        status = "possible_drift"
        severity = "medium"

    else:
        status = "stable"
        severity = "none"

    return {
        "status": status,
        "severity": severity,
        "drift_score": round(
            float(drift_score),
            4
        ),
        "reference_mean": round(
            float(reference_mean),
            4
        ),
        "current_mean": round(
            float(current_mean),
            4
        ),
        "reference_std": round(
            float(reference_std),
            4
        )
    }


def calculate_categorical_drift(
    reference_series,
    current_series
):
    """
    Calculate categorical distribution drift
    using category frequency differences.
    """

    reference = (
        reference_series
        .dropna()
        .astype(str)
        .value_counts(
            normalize=True
        )
    )

    current = (
        current_series
        .dropna()
        .astype(str)
        .value_counts(
            normalize=True
        )
    )

    if len(reference) == 0 or len(current) == 0:
        return {
            "status": "failed",
            "drift_score": 0,
            "message": "Not enough categorical data."
        }

    all_categories = set(
        reference.index
    ).union(
        set(current.index)
    )

    drift_score = 0

    for category in all_categories:

        reference_frequency = reference.get(
            category,
            0
        )

        current_frequency = current.get(
            category,
            0
        )

        drift_score += abs(
            reference_frequency
            - current_frequency
        )

    if drift_score >= 0.5:
        status = "drift_detected"
        severity = "high"

    elif drift_score >= 0.2:
        status = "possible_drift"
        severity = "medium"

    else:
        status = "stable"
        severity = "none"

    return {
        "status": status,
        "severity": severity,
        "drift_score": round(
            float(drift_score),
            4
        )
    }


def detect_data_drift(
    reference_df,
    current_df
):
    """
    Compare reference and current datasets
    and detect distribution drift.
    """

    results = []

    common_columns = list(
        set(reference_df.columns)
        .intersection(
            set(current_df.columns)
        )
    )

    for column in common_columns:

        reference_series = (
            reference_df[column]
        )

        current_series = (
            current_df[column]
        )

        if (
            pd.api.types.is_numeric_dtype(
                reference_series
            )
            and
            pd.api.types.is_numeric_dtype(
                current_series
            )
        ):

            drift_result = calculate_numeric_drift(
                reference_series,
                current_series
            )

        else:

            drift_result = calculate_categorical_drift(
                reference_series,
                current_series
            )

        results.append({
            "column": column,
            "data_type": str(
                reference_series.dtype
            ),
            **drift_result
        })

    return results