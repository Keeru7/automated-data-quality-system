import pandas as pd


def normalize_string_columns(df):
    df = df.copy()

    text_columns = df.select_dtypes(
        include="object"
    ).columns

    for column in text_columns:
        df[column] = (
            df[column]
            .apply(
                lambda value:
                value.strip().lower()
                if isinstance(value, str)
                else value
            )
        )

    return df


def normalize_numeric_columns(df):
    df = df.copy()

    for column in df.columns:

        if df[column].dtype == "object":

            converted = pd.to_numeric(
                df[column],
                errors="coerce"
            )

            original_non_null = df[column].notna().sum()

            converted_non_null = converted.notna().sum()

            if (
                original_non_null > 0
                and converted_non_null / original_non_null >= 0.9
            ):
                df[column] = converted

    return df


def normalize_date_columns(df):
    df = df.copy()

    for column in df.columns:

        if "date" in column.lower():

            converted = pd.to_datetime(
                df[column],
                errors="coerce"
            )

            valid_values = converted.notna().sum()

            total_values = df[column].notna().sum()

            if (
                total_values > 0
                and valid_values / total_values >= 0.8
            ):
                df[column] = converted

    return df


def normalize_categorical_columns(df):
    df = df.copy()

    categorical_columns = df.select_dtypes(
        include="object"
    ).columns

    for column in categorical_columns:

        unique_count = df[column].nunique()

        if unique_count <= 20:

            df[column] = (
                df[column]
                .apply(
                    lambda value:
                    " ".join(value.split())
                    if isinstance(value, str)
                    else value
                )
            )

    return df


def normalize_dataset(df):
    df = normalize_string_columns(df)

    df = normalize_numeric_columns(df)

    df = normalize_date_columns(df)

    df = normalize_categorical_columns(df)

    return df