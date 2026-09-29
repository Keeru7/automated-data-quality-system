import pandas as pd


# 1. Detect the possible meaning of a column
def detect_semantic_meaning(column_name):

    name = column_name.lower().strip()

    if "email" in name or "mail" in name:
        return "email"

    elif "phone" in name or "mobile" in name or "contact" in name:
        return "phone"

    elif "date" in name or "time" in name:
        return "date"

    elif "name" in name:
        return "name"

    elif "id" in name or name.endswith("_id"):
        return "ID"

    elif "address" in name:
        return "address"

    else:
        return "unknown"


# 2. Detect mixed data types
def detect_mixed_type(column):

    value_types = column.dropna().map(type).nunique()

    return value_types > 1


# 3. Check whether the data type is consistent
def check_type_consistency(column):

    if column.dtype == "object":

        numeric_values = pd.to_numeric(
            column,
            errors="coerce"
        )

        non_missing = column.notna().sum()

        numeric_count = numeric_values.notna().sum()

        if non_missing > 0 and numeric_count == non_missing:
            return "Looks numeric but stored as text"

    return "Consistent"


# 4. Check whether values follow a consistent format
def check_format_consistency(column_name, series):

    values = series.dropna().astype(str).str.strip()

    if len(values) == 0:
        return "No data"

    name = column_name.lower()

    # Email format
    if "email" in name or "mail" in name:

        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        valid = values.str.match(
            email_pattern
        ).sum()

        if valid / len(values) < 0.9:
            return "Inconsistent email format"

        return "Consistent"

    # Date format
    if "date" in name or "time" in name:

        parsed_dates = pd.to_datetime(
            values,
            errors="coerce"
        )

        invalid = parsed_dates.isna().sum()

        if invalid > 0:
            return "Inconsistent date format"

        return "Consistent"

    # Numeric values stored as text
    numeric_values = pd.to_numeric(
        values,
        errors="coerce"
    )

    if numeric_values.notna().sum() / len(values) > 0.9:
        return "Numeric values stored as text"

    # Extra spaces
    if (values != series.dropna().astype(str)).any():
        return "Inconsistent spaces"

    return "Consistent"


# 5. Detect possible PII
def detect_pii(column_name, series):

    name = column_name.lower().strip()

    pii_keywords = {

        "email": "Possible email information",

        "phone": "Possible phone information",

        "mobile": "Possible phone information",

        "contact": "Possible contact information",

        "name": "Possible personal name",

        "address": "Possible address information",

        "customer": "Possible customer information",

        "user": "Possible user information"
    }

    for keyword, reason in pii_keywords.items():

        if keyword in name:
            return True, reason

    # Check whether values look like email addresses
    if series.dtype == "object":

        sample = series.dropna().astype(str).head(100)

        email_matches = sample.str.match(
            r"^[\w\.-]+@[\w\.-]+\.\w+$"
        ).sum()

        if len(sample) > 0 and email_matches / len(sample) > 0.5:

            return True, "Values look like email addresses"

    return False, "No obvious PII detected"


# 6. Detect suspicious columns
def detect_suspicious_column(column_name, series):

    reasons = []

    # Missing percentage
    missing_percentage = (
        series.isnull().mean() * 100
    )

    # Unique percentage
    unique_percentage = (
        series.nunique() / len(series)
    ) * 100

    # High missing values
    if missing_percentage > 50:

        reasons.append(
            "High missing values"
        )

    # Very high number of unique values
    if unique_percentage > 95:

        reasons.append(
            "Very high cardinality"
        )

    # Column contains only one value
    if series.nunique() <= 1:

        reasons.append(
            "Constant column"
        )

    # Possible ID column
    name = column_name.lower()

    if "id" in name:

        reasons.append(
            "Possible identifier column"
        )

    if reasons:

        return True, "; ".join(reasons)

    return False, "No major issue detected"