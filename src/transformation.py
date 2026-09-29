import pandas as pd
from sklearn.preprocessing import StandardScaler


def scale_numeric_columns(df):
    df = df.copy()

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    if len(numeric_columns) == 0:
        return df

    scaler = StandardScaler()

    df[numeric_columns] = scaler.fit_transform(
        df[numeric_columns]
    )

    return df


def encode_categorical_columns(df):
    df = df.copy()

    categorical_columns = df.select_dtypes(
        include="object"
    ).columns

    if len(categorical_columns) == 0:
        return df

    df = pd.get_dummies(
        df,
        columns=categorical_columns,
        drop_first=False
    )

    return df


def normalize_numeric_columns(df):
    df = df.copy()

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    for column in numeric_columns:

        minimum = df[column].min()
        maximum = df[column].max()

        if maximum != minimum:

            df[column] = (
                (df[column] - minimum)
                / (maximum - minimum)
            )

    return df


def extract_date_features(df):
    df = df.copy()

    date_columns = df.select_dtypes(
        include=["datetime64[ns]"]
    ).columns

    for column in date_columns:

        df[column + "_year"] = (
            df[column].dt.year
        )

        df[column + "_month"] = (
            df[column].dt.month
        )

        df[column + "_day"] = (
            df[column].dt.day
        )

        df[column + "_day_of_week"] = (
            df[column].dt.dayofweek
        )

    return df


def transform_dataset(df):
    df = extract_date_features(df)

    df = encode_categorical_columns(df)

    df = scale_numeric_columns(df)

    return df