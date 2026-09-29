import pandas as pd

from sklearn.impute import SimpleImputer
from sklearn.impute import KNNImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.linear_model import LinearRegression


def statistical_imputation(df):
    df = df.copy()

    numeric_columns = df.select_dtypes(include="number").columns
    categorical_columns = df.select_dtypes(include="object").columns

    for column in numeric_columns:
        if df[column].isnull().sum() > 0:
            df[column] = df[column].fillna(
                df[column].median()
            )

    for column in categorical_columns:
        if df[column].isnull().sum() > 0:
            mode_values = df[column].mode()

            if len(mode_values) > 0:
                df[column] = df[column].fillna(
                    mode_values.iloc[0]
                )
            else:
                df[column] = df[column].fillna("Unknown")

    return df


def knn_imputation(df, n_neighbors=5):
    df = df.copy()

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    if len(numeric_columns) == 0:
        return df

    imputer = KNNImputer(
        n_neighbors=n_neighbors
    )

    df[numeric_columns] = imputer.fit_transform(
        df[numeric_columns]
    )

    return df


def regression_imputation(df):
    df = df.copy()

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    for target_column in numeric_columns:

        missing_mask = df[target_column].isnull()

        if missing_mask.sum() == 0:
            continue

        other_columns = [
            column
            for column in numeric_columns
            if column != target_column
        ]

        if len(other_columns) == 0:
            continue

        train_data = df.loc[~missing_mask].copy()
        predict_data = df.loc[missing_mask].copy()

        train_data = train_data.dropna(
            subset=other_columns
        )

        if len(train_data) < 10:
            continue

        X_train = train_data[other_columns]
        y_train = train_data[target_column]

        X_predict = predict_data[other_columns]

        imputer = SimpleImputer(
            strategy="median"
        )

        X_train = imputer.fit_transform(X_train)
        X_predict = imputer.transform(X_predict)

        model = LinearRegression()

        model.fit(
            X_train,
            y_train
        )

        predicted_values = model.predict(
            X_predict
        )

        df.loc[
            missing_mask,
            target_column
        ] = predicted_values

    return df


def iterative_imputation(df):
    df = df.copy()

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    if len(numeric_columns) == 0:
        return df

    imputer = IterativeImputer(
        max_iter=10,
        random_state=42
    )

    df[numeric_columns] = imputer.fit_transform(
        df[numeric_columns]
    )

    return df