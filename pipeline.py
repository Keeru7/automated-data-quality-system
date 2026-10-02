import os
import sys
import yaml
import argparse

# Add project folders to Python path
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "src"
        )
    )
)

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "api"
        )
    )
)

from profiling_api import generate_profile
from cleaning import clean_dataset
from validation_pipeline import generate_validation_report
from logger import setup_logger


def load_config(config_file):
    with open(config_file, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def run_pipeline(config):

    input_file = config["input"]["file"]
    output_folder = config["output"]["folder"]

    os.makedirs(output_folder, exist_ok=True)

    # Setup logger
    logger = setup_logger(
        log_file=config["logging"]["file"],
        level=config["logging"]["level"]
    )

    logger.info("Pipeline started.")
    logger.info(f"Input file: {input_file}")
    logger.info(f"Output folder: {output_folder}")

    # Output files
    profiling_report = os.path.join(
        output_folder,
        "profiling_report.json"
    )

    cleaned_file = os.path.join(
        output_folder,
        "cleaned_data.csv"
    )

    cleaning_log = os.path.join(
        output_folder,
        "cleaning_log.json"
    )

    validation_report = os.path.join(
        output_folder,
        "validation_report.json"
    )

    print("\n===================================")
    print(" AUTOMATED DATA QUALITY PIPELINE")
    print("===================================\n")

    try:

        # STEP 1: PROFILING
        if config["profiling"]["enabled"]:

            logger.info("Starting data profiling.")
            print("Step 1/3: Running data profiling...")

            generate_profile(
                input_file,
                profiling_report
            )

            logger.info("Data profiling completed.")
            print("Profiling completed.")
            print(f"Report: {profiling_report}\n")

        # STEP 2: CLEANING
        if config["cleaning"]["enabled"]:

            logger.info("Starting data cleaning.")
            print("Step 2/3: Running data cleaning...")

            cleaned_df, cleaning_log_data = clean_dataset(
                input_file=input_file,
                output_file=cleaned_file,
                log_file=cleaning_log,
                imputation_method=config["cleaning"]["imputation_method"]
            )

            logger.info("Data cleaning completed.")
            print("Cleaning completed.")
            print(f"Cleaned data: {cleaned_file}")
            print(f"Cleaning log: {cleaning_log}\n")

        # STEP 3: VALIDATION
        if config["validation"]["enabled"]:

            logger.info("Starting data validation.")
            print("Step 3/3: Running data validation...")

            generate_validation_report(
                cleaned_file=cleaned_file,
                report_file=validation_report
            )

            logger.info("Data validation completed.")
            print("Validation completed.")
            print(f"Validation report: {validation_report}\n")

        logger.info("Pipeline completed successfully.")

        print("===================================")
        print(" PIPELINE COMPLETED SUCCESSFULLY")
        print("===================================")

    except Exception as error:

        logger.error(
            f"Pipeline failed: {error}",
            exc_info=True
        )

        print("\n===================================")
        print(" PIPELINE FAILED")
        print("===================================")

        print(f"Error: {error}")

        raise


def main():

    parser = argparse.ArgumentParser(
        description="Automated Data Quality Pipeline"
    )

    parser.add_argument(
        "--input",
        help="Path to the input CSV dataset"
    )

    parser.add_argument(
        "--output",
        help="Folder where pipeline results will be saved"
    )

    args = parser.parse_args()

    # Load default YAML configuration
    config_file = os.path.join(
        os.path.dirname(__file__),
        "config",
        "pipeline_config.yaml"
    )

    config = load_config(config_file)

    # Override YAML values if CLI arguments are provided
    if args.input:
        config["input"]["file"] = args.input

    if args.output:
        config["output"]["folder"] = args.output
        config["logging"]["file"] = os.path.join(
            args.output,
            "pipeline.log"
        )

    run_pipeline(config)


if __name__ == "__main__":
    main()