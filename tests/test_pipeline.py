import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "src"
        )
    )
)

from cleaning import clean_dataset


def test_complete_cleaning_pipeline(tmp_path):

    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "cleaned_data.csv"
    log_file = tmp_path / "cleaning_log.json"

    input_file.write_text(
        "Name,Age,Category\n"
        " John ,25,A\n"
        "Alice,30,B\n"
        " John ,25,A\n"
        "Bob,,A\n"
    )

    cleaned_df, cleaning_log = clean_dataset(
        str(input_file),
        str(output_file),
        str(log_file)
    )

    assert output_file.exists()

    assert log_file.exists()

    assert len(cleaned_df) < 4

    assert cleaned_df.isnull().sum().sum() == 0

    assert "quality_before" in cleaning_log

    assert "quality_after" in cleaning_log

    assert "quality_comparison" in cleaning_log

    assert cleaning_log["duplicates_removed"] >= 1