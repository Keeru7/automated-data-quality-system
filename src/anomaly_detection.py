import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler


def detect_isolation_forest_anomalies(
    df,
    contamination=0.05,
    random_state=42
):
    """
    Detect anomalies using Isolation Forest.
    """

    numeric_df = df.select_dtypes(
        include="number"
    ).copy()

    if numeric_df.empty:
        return {
            "status": "failed",
            "message": "No numeric columns available.",
            "anomaly_count": 0,
            "anomaly_percentage": 0,
            "results": []
        }

    numeric_df = numeric_df.fillna(
        numeric_df.median()
    )

    variable_columns = [
        column
        for column in numeric_df.columns
        if numeric_df[column].nunique() > 1
    ]

    numeric_df = numeric_df[variable_columns]

    if numeric_df.empty:
        return {
            "status": "failed",
            "message": "No variable numeric columns available.",
            "anomaly_count": 0,
            "anomaly_percentage": 0,
            "results": []
        }

    model = IsolationForest(
        contamination=contamination,
        random_state=random_state
    )

    predictions = model.fit_predict(
        numeric_df
    )

    anomaly_scores = model.decision_function(
        numeric_df
    )

    results = []

    for position in range(len(predictions)):

        if predictions[position] == -1:
            status = "anomaly"
            severity = "high"
        else:
            status = "normal"
            severity = "none"

        results.append({
            "row": int(numeric_df.index[position]),
            "status": status,
            "severity": severity,
            "anomaly_score": round(
                float(anomaly_scores[position]),
                4
            )
        })

    anomaly_count = sum(
        1
        for result in results
        if result["status"] == "anomaly"
    )

    total_rows = len(results)

    anomaly_percentage = (
        anomaly_count / total_rows * 100
        if total_rows > 0
        else 0
    )

    return {
        "status": "success",
        "method": "Isolation Forest",
        "anomaly_count": anomaly_count,
        "anomaly_percentage": round(
            anomaly_percentage,
            2
        ),
        "total_rows": total_rows,
        "results": results
    }


def detect_lof_anomalies(
    df,
    contamination=0.05,
    n_neighbors=20
):
    """
    Detect anomalies using Local Outlier Factor.

    Duplicate numeric records are removed before
    LOF calculation.
    """

    numeric_df = df.select_dtypes(
        include="number"
    ).copy()

    if numeric_df.empty:
        return {
            "status": "failed",
            "message": "No numeric columns available.",
            "anomaly_count": 0,
            "anomaly_percentage": 0,
            "results": []
        }

    numeric_df = numeric_df.fillna(
        numeric_df.median()
    )

    variable_columns = [
        column
        for column in numeric_df.columns
        if numeric_df[column].nunique() > 1
    ]

    numeric_df = numeric_df[variable_columns]

    if numeric_df.empty:
        return {
            "status": "failed",
            "message": "No variable numeric columns available.",
            "anomaly_count": 0,
            "anomaly_percentage": 0,
            "results": []
        }

    numeric_df["__original_index__"] = numeric_df.index

    unique_df = numeric_df.drop_duplicates(
        subset=variable_columns
    ).copy()

    original_indexes = unique_df[
        "__original_index__"
    ].tolist()

    unique_features = unique_df[
        variable_columns
    ]

    if len(unique_features) < 3:
        return {
            "status": "failed",
            "message": "Not enough unique records for LOF.",
            "anomaly_count": 0,
            "anomaly_percentage": 0,
            "results": []
        }

    actual_neighbors = min(
        n_neighbors,
        len(unique_features) - 1
    )

    if actual_neighbors < 2:
        return {
            "status": "failed",
            "message": "Not enough records for LOF.",
            "anomaly_count": 0,
            "anomaly_percentage": 0,
            "results": []
        }

    model = LocalOutlierFactor(
        n_neighbors=actual_neighbors,
        contamination=contamination
    )

    predictions = model.fit_predict(
        unique_features
    )

    anomaly_scores = (
        model.negative_outlier_factor_
    )

    results = []

    for position in range(len(predictions)):

        if predictions[position] == -1:
            status = "anomaly"
            severity = "high"
        else:
            status = "normal"
            severity = "none"

        results.append({
            "row": int(original_indexes[position]),
            "status": status,
            "severity": severity,
            "lof_score": round(
                float(anomaly_scores[position]),
                4
            )
        })

    anomaly_count = sum(
        1
        for result in results
        if result["status"] == "anomaly"
    )

    total_rows = len(results)

    anomaly_percentage = (
        anomaly_count / total_rows * 100
        if total_rows > 0
        else 0
    )

    return {
        "status": "success",
        "method": "Local Outlier Factor",
        "anomaly_count": anomaly_count,
        "anomaly_percentage": round(
            anomaly_percentage,
            2
        ),
        "total_rows": total_rows,
        "unique_rows_analyzed": total_rows,
        "duplicate_numeric_rows_excluded": (
            len(numeric_df) - len(unique_features)
        ),
        "results": results
    }


def detect_autoencoder_anomalies(
    df,
    contamination=0.05,
    random_state=42
):
    """
    Detect anomalies using an autoencoder-style
    neural network reconstruction model.

    The model learns to reconstruct normal numeric
    patterns. Records with high reconstruction
    error are treated as potential anomalies.
    """

    numeric_df = df.select_dtypes(
        include="number"
    ).copy()

    if numeric_df.empty:
        return {
            "status": "failed",
            "message": "No numeric columns available.",
            "anomaly_count": 0,
            "anomaly_percentage": 0,
            "results": []
        }

    # Fill missing values
    numeric_df = numeric_df.fillna(
        numeric_df.median()
    )

    # Remove constant columns
    variable_columns = [
        column
        for column in numeric_df.columns
        if numeric_df[column].nunique() > 1
    ]

    numeric_df = numeric_df[variable_columns]

    if numeric_df.empty:
        return {
            "status": "failed",
            "message": "No variable numeric columns available.",
            "anomaly_count": 0,
            "anomaly_percentage": 0,
            "results": []
        }

    # Scale the data
    scaler = StandardScaler()

    scaled_data = scaler.fit_transform(
        numeric_df
    )

    # Autoencoder-style neural network
    model = MLPRegressor(
        hidden_layer_sizes=(8, 4, 8),
        activation="relu",
        solver="adam",
        max_iter=100,
        random_state=random_state
    )

    # Train model to reconstruct the input
    model.fit(
        scaled_data,
        scaled_data
    )

    reconstructed_data = model.predict(
        scaled_data
    )

    # Calculate reconstruction error
    reconstruction_error = (
        (scaled_data - reconstructed_data) ** 2
    ).mean(axis=1)

    # Determine anomaly threshold
    threshold = pd.Series(
        reconstruction_error
    ).quantile(
        1 - contamination
    )

    results = []

    for position, error in enumerate(
        reconstruction_error
    ):

        if error >= threshold:
            status = "anomaly"
            severity = "high"
        else:
            status = "normal"
            severity = "none"

        results.append({
            "row": int(numeric_df.index[position]),
            "status": status,
            "severity": severity,
            "reconstruction_error": round(
                float(error),
                6
            )
        })

    anomaly_count = sum(
        1
        for result in results
        if result["status"] == "anomaly"
    )

    total_rows = len(results)

    anomaly_percentage = (
        anomaly_count / total_rows * 100
        if total_rows > 0
        else 0
    )

    return {
        "status": "success",
        "method": "Autoencoder",
        "anomaly_count": anomaly_count,
        "anomaly_percentage": round(
            anomaly_percentage,
            2
        ),
        "threshold": round(
            float(threshold),
            6
        ),
        "total_rows": total_rows,
        "results": results
    }