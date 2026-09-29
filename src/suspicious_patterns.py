import pandas as pd


def create_pattern_result(
    row,
    column,
    rule,
    status,
    severity,
    message
):
    """
    Create a standard suspicious-pattern result.
    """

    return {
        "row": int(row),
        "column": column,
        "rule": rule,
        "status": status,
        "severity": severity,
        "message": message
    }


def detect_negative_values(
    df,
    columns=None
):
    """
    Detect negative values in numeric columns.
    """

    results = []

    if columns is None:
        columns = df.select_dtypes(
            include="number"
        ).columns.tolist()

    for column in columns:

        if column not in df.columns:
            continue

        numeric_values = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        for index, value in numeric_values.items():

            if pd.isna(value):
                continue

            if value < 0:

                results.append(
                    create_pattern_result(
                        row=index,
                        column=column,
                        rule="negative_value",
                        status="failed",
                        severity="high",
                        message=(
                            f"Negative value {value} "
                            f"detected."
                        )
                    )
                )

    return results


def detect_zero_values(
    df,
    columns=None
):
    """
    Detect zero values in selected numeric columns.
    """

    results = []

    if columns is None:
        columns = df.select_dtypes(
            include="number"
        ).columns.tolist()

    for column in columns:

        if column not in df.columns:
            continue

        numeric_values = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        for index, value in numeric_values.items():

            if pd.isna(value):
                continue

            if value == 0:

                results.append(
                    create_pattern_result(
                        row=index,
                        column=column,
                        rule="zero_value",
                        status="warning",
                        severity="low",
                        message=(
                            f"Zero value detected "
                            f"in {column}."
                        )
                    )
                )

    return results


def detect_extreme_values(
    df,
    columns=None,
    multiplier=1.5
):
    """
    Detect statistical outliers using the IQR method.
    """

    results = []

    if columns is None:
        columns = df.select_dtypes(
            include="number"
        ).columns.tolist()

    for column in columns:

        if column not in df.columns:
            continue

        numeric_values = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        valid_values = numeric_values.dropna()

        if len(valid_values) < 4:
            continue

        q1 = valid_values.quantile(0.25)
        q3 = valid_values.quantile(0.75)

        iqr = q3 - q1

        lower_limit = (
            q1 - multiplier * iqr
        )

        upper_limit = (
            q3 + multiplier * iqr
        )

        for index, value in numeric_values.items():

            if pd.isna(value):
                continue

            if (
                value < lower_limit
                or value > upper_limit
            ):

                results.append(
                    create_pattern_result(
                        row=index,
                        column=column,
                        rule="extreme_value",
                        status="warning",
                        severity="medium",
                        message=(
                            f"Value {value} is "
                            f"outside the expected "
                            f"IQR range."
                        )
                    )
                )

    return results


def validate_total_spent(
    df,
    price_column="Price Per Unit",
    quantity_column="Quantity",
    total_column="Total Spent"
):
    """
    Check whether Total Spent is approximately
    equal to Price Per Unit multiplied by Quantity.
    """

    results = []

    required_columns = [
        price_column,
        quantity_column,
        total_column
    ]

    if not all(
        column in df.columns
        for column in required_columns
    ):
        return results

    price = pd.to_numeric(
        df[price_column],
        errors="coerce"
    )

    quantity = pd.to_numeric(
        df[quantity_column],
        errors="coerce"
    )

    total = pd.to_numeric(
        df[total_column],
        errors="coerce"
    )

    expected_total = price * quantity

    for index in df.index:

        if (
            pd.isna(price.loc[index])
            or pd.isna(quantity.loc[index])
            or pd.isna(total.loc[index])
        ):
            continue

        difference = abs(
            expected_total.loc[index]
            - total.loc[index]
        )

        # Small floating-point differences are allowed.
        if difference > 0.01:

            results.append(
                create_pattern_result(
                    row=index,
                    column=total_column,
                    rule="total_spent_consistency",
                    status="failed",
                    severity="high",
                    message=(
                        f"Total Spent "
                        f"({total.loc[index]}) does not "
                        f"match Price Per Unit × "
                        f"Quantity "
                        f"({expected_total.loc[index]})."
                    )
                )
            )

    return results


def detect_suspicious_patterns(df):
    """
    Run all suspicious-pattern checks.
    """

    results = []

    results.extend(
        detect_negative_values(df)
    )

    results.extend(
        detect_zero_values(df)
    )

    results.extend(
        detect_extreme_values(df)
    )

    results.extend(
        validate_total_spent(df)
    )

    return results