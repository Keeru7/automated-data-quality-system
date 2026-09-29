import logging
import os


def setup_logger(
    log_file="results/pipeline.log",
    level="INFO"
):
    # Create the folder for the log file
    log_directory = os.path.dirname(log_file)

    if log_directory:
        os.makedirs(log_directory, exist_ok=True)

    # Convert text level to logging level
    log_level = getattr(
        logging,
        level.upper(),
        logging.INFO
    )

    # Create logger
    logger = logging.getLogger("data_quality_pipeline")

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(log_level)

    # File handler
    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8"
    )

    # Console handler
    console_handler = logging.StreamHandler()

    # Log format
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger