import pandas as pd
from rapidfuzz.fuzz import ratio


def find_exact_duplicates(df):
    duplicate_count = int(df.duplicated().sum())

    return duplicate_count


def normalize_text(value):
    if pd.isna(value):
        return ""

    value = str(value)

    value = value.strip().lower()

    value = " ".join(value.split())

    return value


def find_fuzzy_duplicates(df, threshold=90):
    df = df.copy()

    text_columns = df.select_dtypes(
        include="object"
    ).columns.tolist()

    if len(text_columns) == 0:
        return []

    # Create normalized text for comparison
    normalized_values = []

    for index, row in df.iterrows():

        row_values = []

        for column in text_columns:
            value = normalize_text(
                row[column]
            )

            row_values.append(value)

        combined_value = " | ".join(row_values)

        normalized_values.append(
            (index, combined_value)
        )

    fuzzy_duplicates = []

    # Compare records
    for i in range(len(normalized_values)):

        index_1, value_1 = normalized_values[i]

        for j in range(i + 1, len(normalized_values)):

            index_2, value_2 = normalized_values[j]

            similarity = ratio(
                value_1,
                value_2
            )

            if similarity >= threshold:

                fuzzy_duplicates.append({
                    "row_1": int(index_1),
                    "row_2": int(index_2),
                    "similarity": round(
                        similarity,
                        2
                    )
                })

    return fuzzy_duplicates