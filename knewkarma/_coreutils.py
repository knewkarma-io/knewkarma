# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

import csv
import json
import logging
import os
from typing import Union, List

from ._metadata import (
    CSV_DIRECTORY,
    JSON_DIRECTORY,
)
from ._parser import create_parser


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def pathfinder():
    """
    Creates file directories in the specified target_directory, if they don't already exist.
    """
    directories: list = [
        CSV_DIRECTORY,
        JSON_DIRECTORY,
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def save_data(
    data: Union[dict, List[dict]],
    filename: str,
    save_to_json: bool = False,
    save_to_csv: bool = False,
):
    """
    Save the given data to JSON and/or CSV files based on the arguments.

    :param data: The data to be saved, which can be a dict or a list of dicts.
    :param filename: The base filename to use when saving.
    :param save_to_json: A boolean value to indicate whether to save data as a JSON file.
    :param save_to_csv: A boolean value to indicate whether to save data as a CSV file.
    """
    if save_to_json:
        json_path = os.path.join(JSON_DIRECTORY, f"{filename}.json")
        with open(json_path, "w") as json_file:
            json.dump(data, json_file, indent=4)
        log.info(f"{os.path.getsize(json_file.name)} bytes written to {json_file.name}")

    if save_to_csv:
        csv_path = os.path.join(CSV_DIRECTORY, f"{filename}.csv")
        with open(csv_path, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            if isinstance(data, dict):
                writer.writerow(data.keys())
                writer.writerow(data.values())
            elif isinstance(data, list):
                if data:
                    writer.writerow(
                        data[0].keys()
                    )  # header from keys of the first item
                    for item in data:
                        writer.writerow(item.values())
        log.info(f"{os.path.getsize(csv_file.name)} bytes written to {csv_file.name}")


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


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
                markup=True, log_time_format="[%I:%M:%S %p]", show_level=debug_mode
            )
        ],
    )
    return logging.getLogger("Knew Karma")


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

log: logging = setup_logging(debug_mode=create_parser().parse_args().debug)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
