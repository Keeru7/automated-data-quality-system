import pandas as pd


def calculate_quality_score(df):
    """
    Calculate overall data quality score.
    Score is based on missing values and duplicate rows.
    """

    total_cells = df.shape[0] * df.shape[1]

    if total_cells == 0:
        return 0

    # Missing value percentage
    missing_cells = df.isnull().sum().sum()
    missing_percentage = (missing_cells / total_cells) * 100

    # Duplicate row percentage
    duplicate_rows = df.duplicated().sum()

    if len(df) > 0:
        duplicate_percentage = (duplicate_rows / len(df)) * 100
    else:
        duplicate_percentage = 0

    # Individual scores
    completeness_score = 100 - missing_percentage
    duplicate_score = 100 - duplicate_percentage

    # Overall quality score
    quality_score = (
        completeness_score * 0.6
        + duplicate_score * 0.4
    )

    return round(quality_score, 2)


def get_quality_metrics(df):
    """
    Return detailed data quality metrics.
    """

    total_cells = df.shape[0] * df.shape[1]

    if total_cells == 0:
        return {
            "quality_score": 0,
            "missing_cells": 0,
            "missing_percentage": 0,
            "duplicate_rows": 0,
            "duplicate_percentage": 0
        }

    missing_cells = int(df.isnull().sum().sum())
    missing_percentage = (missing_cells / total_cells) * 100

    duplicate_rows = int(df.duplicated().sum())
    duplicate_percentage = (
        duplicate_rows / len(df) * 100
        if len(df) > 0
        else 0
    )

    quality_score = calculate_quality_score(df)

    return {
        "quality_score": quality_score,
        "missing_cells": missing_cells,
        "missing_percentage": round(missing_percentage, 2),
        "duplicate_rows": duplicate_rows,
        "duplicate_percentage": round(duplicate_percentage, 2)
    }


def compare_quality_scores(before_score, after_score):
    """
    Compare quality before and after cleaning.
    """

    quality_delta = after_score - before_score

    return {
        "score_before": before_score,
        "score_after": after_score,
        "quality_delta": round(quality_delta, 2)
    }