import json
import os
import pandas as pd

from validation_rules import (
    validate_dataset_structure,
    validate_missing_values
)

from anomaly_detection import (
    detect_isolation_forest_anomalies,
    detect_lof_anomalies,
    detect_autoencoder_anomalies
)

from suspicious_patterns import (
    detect_suspicious_patterns
)

from data_drift import (
    detect_data_drift
)

from severity_scoring import (
    generate_severity_report
)

from model_evaluation import (
    evaluate_anomaly_predictions,
    calculate_roc_curve
)


# ============================================================
# MODEL EVALUATION
# ============================================================

def generate_evaluation_results():

    """
    Generate demonstration evaluation results.

    IMPORTANT:
    These are demonstration labels only.
    They are NOT ground-truth labels from
    the retail dataset.
    """

    actual_labels = [
        0, 0, 0, 1, 0,
        0, 0, 1, 0, 0,
        0, 0, 0, 1, 0,
        0, 0, 0, 0, 0
    ]

    predicted_labels = [
        0, 0, 0, 1, 0,
        0, 1, 1, 0, 0,
        0, 0, 1, 0, 0,
        0, 0, 0, 0, 0
    ]

    anomaly_scores = [
        0.10,
        0.20,
        0.15,
        0.90,
        0.30,
        0.25,
        0.80,
        0.95,
        0.20,
        0.10,
        0.15,
        0.25,
        0.85,
        0.20,
        0.15,
        0.10,
        0.20,
        0.15,
        0.10
    ]

    # --------------------------------------------------------
    # Safety check
    # --------------------------------------------------------

    minimum_length = min(
        len(actual_labels),
        len(predicted_labels),
        len(anomaly_scores)
    )

    actual_labels = actual_labels[:minimum_length]

    predicted_labels = predicted_labels[:minimum_length]

    anomaly_scores = anomaly_scores[:minimum_length]

    # --------------------------------------------------------
    # Classification evaluation
    # --------------------------------------------------------

    evaluation = evaluate_anomaly_predictions(
        actual_labels,
        predicted_labels
    )

    # --------------------------------------------------------
    # ROC evaluation
    # --------------------------------------------------------

    roc_result = calculate_roc_curve(
        actual_labels,
        anomaly_scores
    )

    return {

        "note": (
            "Demonstration evaluation labels "
            "used to verify the evaluation framework. "
            "They are not ground-truth labels from "
            "the retail dataset."
        ),

        "precision": evaluation[
            "precision"
        ],

        "recall": evaluation[
            "recall"
        ],

        "confusion_matrix": evaluation[
            "confusion_matrix"
        ],

        "classification_report": evaluation[
            "classification_report"
        ],

        "roc_auc": roc_result[
            "auc"
        ],

        "roc_curve": {

            "false_positive_rate":
                roc_result[
                    "false_positive_rate"
                ],

            "true_positive_rate":
                roc_result[
                    "true_positive_rate"
                ],

            "thresholds":
                roc_result[
                    "thresholds"
                ]
        }
    }


# ============================================================
# VALIDATION PIPELINE
# ============================================================

def generate_validation_report(
    cleaned_file,
    report_file,
    reference_file=None
):

    """
    Generate a complete validation report
    for a cleaned dataset.
    """

    # --------------------------------------------------------
    # 1. Load cleaned dataset
    # --------------------------------------------------------

    df = pd.read_csv(
        cleaned_file
    )

    # --------------------------------------------------------
    # 2. Rule-based validation
    # --------------------------------------------------------

    rule_results = []

    rule_results.extend(
        validate_dataset_structure(df)
    )

    rule_results.extend(
        validate_missing_values(df)
    )

    # --------------------------------------------------------
    # 3. Suspicious pattern detection
    # --------------------------------------------------------

    suspicious_results = (
        detect_suspicious_patterns(df)
    )

    # --------------------------------------------------------
    # 4. Isolation Forest
    # --------------------------------------------------------

    isolation_forest = (
        detect_isolation_forest_anomalies(
            df
        )
    )

    # --------------------------------------------------------
    # 5. Local Outlier Factor
    # --------------------------------------------------------

    lof = (
        detect_lof_anomalies(
            df
        )
    )

    # --------------------------------------------------------
    # 6. Autoencoder
    # --------------------------------------------------------

    autoencoder = (
        detect_autoencoder_anomalies(
            df
        )
    )

    # --------------------------------------------------------
    # 7. Data drift
    # --------------------------------------------------------

    drift_results = []

    if reference_file is not None:

        reference_df = pd.read_csv(
            reference_file
        )

        drift_results = detect_data_drift(
            reference_df,
            df
        )

    # --------------------------------------------------------
    # 8. Combine findings
    # --------------------------------------------------------

    all_findings = []

    all_findings.extend(
        rule_results
    )

    all_findings.extend(
        suspicious_results
    )

    # --------------------------------------------------------
    # 9. Isolation Forest findings
    # --------------------------------------------------------

    if isolation_forest.get(
        "status"
    ) == "success":

        for result in isolation_forest[
            "results"
        ]:

            if result["status"] == "anomaly":

                all_findings.append({

                    "row":
                        result["row"],

                    "column":
                        "dataset",

                    "rule":
                        "isolation_forest",

                    "status":
                        "anomaly",

                    "severity":
                        result["severity"],

                    "message":
                        (
                            "Potential anomaly detected "
                            "by Isolation Forest."
                        )
                })

    # --------------------------------------------------------
    # 10. LOF findings
    # --------------------------------------------------------

    if lof.get(
        "status"
    ) == "success":

        for result in lof[
            "results"
        ]:

            if result["status"] == "anomaly":

                all_findings.append({

                    "row":
                        result["row"],

                    "column":
                        "dataset",

                    "rule":
                        "local_outlier_factor",

                    "status":
                        "anomaly",

                    "severity":
                        result["severity"],

                    "message":
                        (
                            "Potential anomaly detected "
                            "by Local Outlier Factor."
                        )
                })

    # --------------------------------------------------------
    # 11. Autoencoder findings
    # --------------------------------------------------------

    if autoencoder.get(
        "status"
    ) == "success":

        for result in autoencoder[
            "results"
        ]:

            if result["status"] == "anomaly":

                all_findings.append({

                    "row":
                        result["row"],

                    "column":
                        "dataset",

                    "rule":
                        "autoencoder",

                    "status":
                        "anomaly",

                    "severity":
                        result["severity"],

                    "message":
                        (
                            "Potential anomaly detected "
                            "by Autoencoder."
                        )
                })

    # --------------------------------------------------------
    # 12. Severity and health score
    # --------------------------------------------------------

    severity_report = (
        generate_severity_report(
            all_findings
        )
    )

    # --------------------------------------------------------
    # 13. Model evaluation
    # --------------------------------------------------------

    evaluation_results = (
        generate_evaluation_results()
    )

    # --------------------------------------------------------
    # 14. Final validation report
    # --------------------------------------------------------

    validation_report = {

        "dataset": {

            "file_name":
                os.path.basename(
                    cleaned_file
                ),

            "total_rows":
                len(df),

            "total_columns":
                len(df.columns)
        },

        "rule_validation": {

            "total_findings":
                len(rule_results),

            "results":
                rule_results
        },

        "suspicious_patterns": {

            "total_findings":
                len(suspicious_results),

            "results":
                suspicious_results
        },

        "anomaly_detection": {

            "isolation_forest":
                isolation_forest,

            "local_outlier_factor":
                lof,

            "autoencoder":
                autoencoder
        },

        "data_drift": {

            "reference_file":
                reference_file,

            "results":
                drift_results
        },

        "severity_and_health":
            severity_report,

        "model_evaluation":
            evaluation_results
    }

    # --------------------------------------------------------
    # 15. Create report directory
    # --------------------------------------------------------

    report_directory = os.path.dirname(
        report_file
    )

    if report_directory:

        os.makedirs(
            report_directory,
            exist_ok=True
        )

    # --------------------------------------------------------
    # 16. Save JSON report
    # --------------------------------------------------------

    with open(
        report_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            validation_report,
            file,
            indent=4,
            default=str
        )

    # --------------------------------------------------------
    # 17. Return report
    # --------------------------------------------------------

    return validation_report