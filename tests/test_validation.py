import pandas as pd

from validation_rules import (
    validate_dataset_structure,
    validate_missing_values,
    validate_email_column,
    validate_phone_column,
    validate_postcode_column,
    validate_numeric_range,
    validate_categorical_consistency
)

from suspicious_patterns import (
    detect_negative_values,
    detect_zero_values,
    validate_total_spent
)

from severity_scoring import (
    calculate_health_score
)


def test_dataset_structure():

    df = pd.DataFrame({
        "Name": ["A", "B", "C"]
    })

    results = validate_dataset_structure(df)

    assert results[0]["status"] == "passed"


def test_missing_values():

    df = pd.DataFrame({
        "Name": ["A", None, "C"]
    })

    results = validate_missing_values(df)

    assert len(results) > 0
    assert results[0]["status"] == "failed"


def test_email_validation():

    df = pd.DataFrame({
        "Email": [
            "test@gmail.com",
            "wrong-email"
        ]
    })

    results = validate_email_column(
        df,
        "Email"
    )

    failed_results = [
        result
        for result in results
        if result["status"] == "failed"
    ]

    assert len(failed_results) == 1


def test_phone_validation():

    df = pd.DataFrame({
        "Phone": [
            "9876543210",
            "12345"
        ]
    })

    results = validate_phone_column(
        df,
        "Phone"
    )

    failed_results = [
        result
        for result in results
        if result["status"] == "failed"
    ]

    assert len(failed_results) == 1


def test_postcode_validation():

    df = pd.DataFrame({
        "Postcode": [
            "500001",
            "123"
        ]
    })

    results = validate_postcode_column(
        df,
        "Postcode"
    )

    failed_results = [
        result
        for result in results
        if result["status"] == "failed"
    ]

    assert len(failed_results) == 1


def test_numeric_range():

    df = pd.DataFrame({
        "Age": [
            20,
            30,
            150
        ]
    })

    results = validate_numeric_range(
        df,
        "Age",
        minimum=0,
        maximum=100
    )

    failed_results = [
        result
        for result in results
        if result["status"] == "failed"
    ]

    assert len(failed_results) == 1


def test_categorical_consistency():

    df = pd.DataFrame({
        "Category": [
            "Food",
            "Clothing",
            "Unknown"
        ]
    })

    results = validate_categorical_consistency(
        df,
        "Category",
        [
            "Food",
            "Clothing"
        ]
    )

    failed_results = [
        result
        for result in results
        if result["status"] == "failed"
    ]

    assert len(failed_results) == 1


def test_negative_value_detection():

    df = pd.DataFrame({
        "Price": [
            10,
            -5,
            20
        ]
    })

    results = detect_negative_values(
        df
    )

    assert len(results) == 1


def test_zero_value_detection():

    df = pd.DataFrame({
        "Quantity": [
            2,
            0,
            5
        ]
    })

    results = detect_zero_values(
        df
    )

    assert len(results) == 1


def test_total_spent_validation():

    df = pd.DataFrame({
        "Price Per Unit": [
            10,
            20
        ],

        "Quantity": [
            2,
            3
        ],

        "Total Spent": [
            20,
            100
        ]
    })

    results = validate_total_spent(
        df
    )

    assert len(results) == 1


def test_health_score():

    results = [
        {
            "severity": "high"
        },
        {
            "severity": "medium"
        },
        {
            "severity": "low"
        }
    ]

    score = calculate_health_score(
        results
    )

    assert score == 91