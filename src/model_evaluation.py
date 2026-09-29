import numpy as np

from sklearn.metrics import (
    precision_score,
    recall_score,
    confusion_matrix,
    classification_report
)


def evaluate_anomaly_predictions(
    actual_labels,
    predicted_labels
):
    """
    Calculate precision, recall and
    confusion matrix for anomaly detection.

    Labels:
    0 = normal
    1 = anomaly
    """

    precision = precision_score(
        actual_labels,
        predicted_labels,
        zero_division=0
    )

    recall = recall_score(
        actual_labels,
        predicted_labels,
        zero_division=0
    )

    matrix = confusion_matrix(
        actual_labels,
        predicted_labels
    )

    report = classification_report(
        actual_labels,
        predicted_labels,
        labels=[0, 1],
        target_names=[
            "normal",
            "anomaly"
        ],
        zero_division=0
    )

    return {
        "precision": round(
            float(precision),
            4
        ),
        "recall": round(
            float(recall),
            4
        ),
        "confusion_matrix": matrix.tolist(),
        "classification_report": report
    }


def create_demo_labels(
    total_rows,
    anomaly_indexes
):
    """
    Create evaluation labels for testing.

    0 = normal
    1 = anomaly
    """

    labels = np.zeros(
        total_rows,
        dtype=int
    )

    for index in anomaly_indexes:

        if 0 <= index < total_rows:
            labels[index] = 1

    return labels.tolist()
import matplotlib.pyplot as plt

from sklearn.metrics import (
    roc_curve,
    roc_auc_score
)


def calculate_roc_curve(
    actual_labels,
    anomaly_scores
):
    """
    Calculate ROC curve and AUC score.

    Higher anomaly score means
    greater likelihood of anomaly.
    """

    false_positive_rate, true_positive_rate, thresholds = (
        roc_curve(
            actual_labels,
            anomaly_scores
        )
    )

    auc_score = roc_auc_score(
        actual_labels,
        anomaly_scores
    )

    return {
        "false_positive_rate": false_positive_rate.tolist(),
        "true_positive_rate": true_positive_rate.tolist(),
        "thresholds": thresholds.tolist(),
        "auc": round(
            float(auc_score),
            4
        )
    }


def plot_roc_curve(
    actual_labels,
    anomaly_scores
):
    """
    Plot the ROC curve.
    """

    false_positive_rate, true_positive_rate, _ = (
        roc_curve(
            actual_labels,
            anomaly_scores
        )
    )

    auc_score = roc_auc_score(
        actual_labels,
        anomaly_scores
    )

    plt.figure()

    plt.plot(
        false_positive_rate,
        true_positive_rate,
        label=f"ROC Curve (AUC = {auc_score:.2f})"
    )

    plt.plot(
        [0, 1],
        [0, 1],
        linestyle="--"
    )

    plt.xlabel(
        "False Positive Rate"
    )

    plt.ylabel(
        "True Positive Rate"
    )

    plt.title(
        "Anomaly Detection ROC Curve"
    )

    plt.legend()

    plt.show()