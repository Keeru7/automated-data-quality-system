import sys
import os

import pandas as pd

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "src"
        )
    )
)

from cleaning import remove_duplicates
from quality_scoring import calculate_quality_score
from schema_inference import infer_schema
from normalization import normalize_string_columns
from imputation import statistical_imputation


def test_remove_duplicates():

    df = pd.DataFrame({
        "Name": ["John", "John", "Alice"],
        "Age": [25, 25, 30]
    })

    cleaned_df, removed = remove_duplicates(df)

    assert removed == 1
    assert len(cleaned_df) == 2


def test_quality_score():

    df = pd.DataFrame({
        "Name": ["John", "Alice"],
        "Age": [25, 30]
    })

    score = calculate_quality_score(df)

    assert score == 100


def test_schema_inference():

    df = pd.DataFrame({
        "Customer_ID": [1, 2, 3],
        "Age": [25, 30, 35],
        "Category": ["A", "B", "A"]
    })

    schema = infer_schema(df)

    assert len(schema) == 3
    assert schema[0]["column_name"] == "Customer_ID"


def test_string_normalization():

    df = pd.DataFrame({
        "Name": [" John ", " ALICE "]
    })

    result = normalize_string_columns(df)

    assert result["Name"].tolist() == [
        "john",
        "alice"
    ]


def test_statistical_imputation():

    df = pd.DataFrame({
        "Age": [20, 30, None, 40]
    })

    result = statistical_imputation(df)

    assert result["Age"].isnull().sum() == 0