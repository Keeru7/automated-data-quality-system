import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "src"
        )
    )
)

from validation_pipeline import (
    generate_validation_report
)


def run_validation_api(
    cleaned_file,
    report_file,
    reference_file=None
):
    """
    Run the complete validation pipeline
    through an API-style function.
    """

    report = generate_validation_report(
        cleaned_file=cleaned_file,
        report_file=report_file,
        reference_file=reference_file
    )

    health_info = report[
        "severity_and_health"
    ]

    return {
        "status": "success",
        "message": (
            "Dataset validation completed successfully."
        ),
        "input_file": cleaned_file,
        "report_file": report_file,
        "total_findings": health_info[
            "total_findings"
        ],
        "health_score": health_info[
            "health_score"
        ],
        "health_status": health_info[
            "health_status"
        ]
    }