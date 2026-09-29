import pandas as pd
import re


def classify_column_name(column_name):
    """
    Classify the semantic meaning of a column
    using its name.
    """

    name = column_name.lower().strip()

    patterns = {
        "email": [
            "email",
            "e-mail",
            "mail"
        ],

        "phone": [
            "phone",
            "mobile",
            "contact",
            "telephone"
        ],

        "postcode": [
            "postcode",
            "postal",
            "zip",
            "pincode",
            "pin_code"
        ],

        "date": [
            "date",
            "time",
            "timestamp"
        ],

        "identifier": [
            "id",
            "code",
            "number"
        ],

        "name": [
            "name",
            "customer_name",
            "product_name"
        ],

        "address": [
            "address",
            "street",
            "location"
        ],

        "category": [
            "category",
            "type",
            "class",
            "segment"
        ],

        "quantity": [
            "quantity",
            "qty",
            "count",
            "units"
        ],

        "price": [
            "price",
            "cost",
            "amount",
            "revenue",
            "sales",
            "spent"
        ],

        "payment_method": [
            "payment",
            "payment_method"
        ]
    }

    for meaning, keywords in patterns.items():

        for keyword in keywords:

            if keyword in name:
                return meaning

    return "unknown"


def classify_value_pattern(series):
    """
    Identify semantic meaning from actual values.
    """

    values = (
        series
        .dropna()
        .astype(str)
        .str.strip()
    )

    if len(values) == 0:
        return "unknown"

    sample = values.head(100)

    # Email detection
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    email_matches = sample.str.match(
        email_pattern
    ).sum()

    if email_matches / len(sample) >= 0.7:
        return "email"

    # Phone detection
    phone_matches = 0

    for value in sample:

        digits = re.sub(
            r"\D",
            "",
            value
        )

        if 10 <= len(digits) <= 15:
            phone_matches += 1

    if phone_matches / len(sample) >= 0.7:
        return "phone"

    # Date detection
    # Only attempt date parsing when the
    # column name suggests a date/time field.
    column_name = str(series.name).lower()

    date_keywords = [
        "date",
        "time",
        "timestamp"
    ]

    looks_like_date_column = any(
        keyword in column_name
        for keyword in date_keywords
    )

    if looks_like_date_column:

        parsed_dates = pd.to_datetime(
            sample,
            errors="coerce",
            format="mixed"
        )

        if (
            parsed_dates.notna().sum()
            / len(sample)
            >= 0.8
        ):
            return "date"

    # Numeric values
    numeric_values = pd.to_numeric(
        sample,
        errors="coerce"
    )

    if (
        numeric_values.notna().sum()
        / len(sample)
        >= 0.9
    ):
        return "numeric"

    # Categorical values
    unique_ratio = (
        sample.nunique()
        / len(sample)
    )

    if unique_ratio <= 0.2:
        return "categorical"

    return "text"


def classify_columns(df):
    """
    Classify all columns using both
    column names and value patterns.
    """

    results = []

    for column in df.columns:

        name_prediction = classify_column_name(
            column
        )

        value_prediction = classify_value_pattern(
            df[column]
        )

        if value_prediction != "unknown":

            detected_meaning = value_prediction

        else:

            detected_meaning = name_prediction

        results.append({
            "column": column,
            "name_based_meaning": name_prediction,
            "value_based_meaning": value_prediction,
            "detected_meaning": detected_meaning
        })

    return results


def detect_semantic_inconsistencies(df):
    """
    Detect possible semantic inconsistencies
    between column names and their values.
    """

    classifications = classify_columns(df)

    inconsistencies = []

    compatible_meanings = {
        "email": ["email"],
        "phone": ["phone"],
        "postcode": [
            "postcode",
            "numeric"
        ],
        "date": ["date"],
        "name": [
            "name",
            "text"
        ],
        "address": [
            "address",
            "text"
        ],
        "category": [
            "category",
            "categorical"
        ],
        "quantity": [
            "quantity",
            "numeric"
        ],
        "price": [
            "price",
            "numeric"
        ],
        "payment_method": [
            "payment_method",
            "categorical"
        ],
        "identifier": [
            "identifier",
            "numeric",
            "text"
        ]
    }

    for item in classifications:

        name_meaning = item[
            "name_based_meaning"
        ]

        value_meaning = item[
            "value_based_meaning"
        ]

        if name_meaning in compatible_meanings:

            expected_values = compatible_meanings[
                name_meaning
            ]

            if value_meaning not in expected_values:

                inconsistencies.append({
                    "column": item["column"],
                    "expected_meaning": name_meaning,
                    "detected_value_meaning": value_meaning,
                    "status": "inconsistent",
                    "severity": "medium",
                    "message": (
                        f"Column name suggests "
                        f"'{name_meaning}', but "
                        f"values appear to represent "
                        f"'{value_meaning}'."
                    )
                })

    return inconsistencies