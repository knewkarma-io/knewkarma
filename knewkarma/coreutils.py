import csv
import json
import logging
import os
from datetime import datetime

from . import CSV_DIRECTORY, JSON_DIRECTORY
from .parser import create_parser


def path_finder():
    """
    Creates file directories if they don't already exist.
    """
    file_directories: list = [CSV_DIRECTORY, JSON_DIRECTORY]
    for directory in file_directories:
        os.makedirs(directory, exist_ok=True)


def save_data(
    data: dict,
    filename: str,
    save_to_json: bool = False,
    save_to_csv: bool = False,
):
    """
    Save the given data to JSON and/or CSV files based on the arguments.

    :param data: The data to be saved, which is a list of dictionaries.
    :param filename: The base filename to use when saving.
    :param save_to_json: A boolean value to indicate whether to save data as a JSON file.
    :param save_to_csv: A boolean value to indicate whether to save data as a CSV file.
    """
    # Save to JSON if save_json is True
    if save_to_json:
        with open(os.path.join(JSON_DIRECTORY, f"{filename}.json"), "w") as json_file:
            json.dump(data, json_file)
        log.info(f"JSON data saved to {json_file.name}")

    # Save to CSV if save_csv is True
    if save_to_csv:
        with open(
            os.path.join(CSV_DIRECTORY, f"{filename}.csv"), "w", newline=""
        ) as csv_file:
            writer = csv.writer(csv_file)
            # Write the header based on keys from the first dictionary
            header = data.keys()
            writer.writerow(header)

            # Write each row
            writer.writerow(data.values())
        log.info(f"CSV data saved to {csv_file.name}")


def convert_timestamp_to_datetime(timestamp: float) -> str:
    """
    Converts a Unix timestamp to a formatted datetime string.

    :param timestamp: The Unix timestamp to be converted.
    :return: A formatted datetime string in the format "dd MMMM yyyy, hh:mm:ssAM/PM".
    """
    utc_from_timestamp: datetime = datetime.fromtimestamp(timestamp)
    datetime_object: utc_from_timestamp = utc_from_timestamp.strftime(
        "%d %B %Y, %I:%M:%S%p"
    )
    return datetime_object


def setup_logging(debug_mode: bool) -> logging.getLogger:
    """
    Configure and return a logging object with the specified log level.

    :param debug_mode: A boolean value indicating whether log level should be set to DEBUG.
    :return: A logging object configured with the specified log level.
    """
    from rich.logging import RichHandler

    logging.basicConfig(
        level="NOTSET" if debug_mode else "INFO",
        format="%(message)s",
        handlers=[
            RichHandler(
                markup=True, log_time_format="(%H:%M:%S)", show_level=debug_mode
            )
        ],
    )
    return logging.getLogger("Knew Karma")


log: logging = setup_logging(debug_mode=create_parser().parse_args().debug)
