import os
import pandas as pd

from validation_pipeline import (
    generate_validation_report
)


def test_complete_validation_pipeline():

    # Create a small test dataset
    test_data = pd.DataFrame({
        "Product": [
            "Apple",
            "Shirt",
            "Rice",
            "Laptop",
            "Pen"
        ],

        "Quantity": [
            2,
            3,
            5,
            1,
            10
        ],

        "Price Per Unit": [
            10,
            500,
            100,
            50000,
            20
        ],

        "Total Spent": [
            20,
            1500,
            500,
            50000,
            200
        ]
    })

    # Temporary input and output files
    input_file = "test_validation_input.csv"

    output_file = "test_validation_report.json"

    # Save test dataset
    test_data.to_csv(
        input_file,
        index=False
    )

    # Generate validation report
    report = generate_validation_report(
        cleaned_file=input_file,
        report_file=output_file
    )

    # Check report was generated
    assert report is not None

    # Check important sections exist
    assert "dataset" in report

    assert "rule_validation" in report

    assert "suspicious_patterns" in report

    assert "anomaly_detection" in report

    assert "data_drift" in report

    assert "severity_and_health" in report

    assert "model_evaluation" in report

    # Check saved JSON file
    assert os.path.exists(
        output_file
    )

    # Clean up test files
    if os.path.exists(input_file):

        os.remove(
            input_file
        )

    if os.path.exists(output_file):

        os.remove(
            output_file
        )