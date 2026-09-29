import pandas as pd


def infer_expected_type(column_name, series):
    name = column_name.lower()

    if "date" in name or "time" in name:
        return "date"

    if "id" in name:
        return "identifier"

    if series.dtype in ["int64", "float64"]:
        return "numeric"

    if series.dtype == "object":
        unique_values = series.dropna().astype(str).nunique()

        if unique_values < 20:
            return "categorical"

        return "string"

    return str(series.dtype)


def infer_expected_range(column_name, series):
    if pd.api.types.is_numeric_dtype(series):
        return {
            "minimum": float(series.min()),
            "maximum": float(series.max())
        }

    return None


def infer_expected_format(column_name, series):
    name = column_name.lower()

    if "date" in name or "time" in name:
        return "YYYY-MM-DD"

    if "email" in name or "mail" in name:
        return "email format"

    if "phone" in name or "mobile" in name:
        return "phone format"

    if series.dtype == "object":
        return "text"

    if pd.api.types.is_numeric_dtype(series):
        return "numeric"

    return "unknown"


def infer_schema(df):
    schema = []

    for column in df.columns:
        series = df[column]

        expected_type = infer_expected_type(
            column,
            series
        )

        expected_range = infer_expected_range(
            column,
            series
        )

        expected_format = infer_expected_format(
            column,
            series
        )

        schema.append({
            "column_name": column,
            "expected_type": expected_type,
            "expected_range": expected_range,
            "expected_format": expected_format
        })

    return schema