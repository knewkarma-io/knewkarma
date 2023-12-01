# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

import csv
import json
import logging
import os

from ._parser import create_parser
from .metadata import (
    CSV_DIRECTORY,
    JSON_DIRECTORY,
)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def pathfinder():
    """
    Creates file directories in the user's home directory, if they don't already exist.
    """
    directories: list = [
        CSV_DIRECTORY,
        JSON_DIRECTORY,
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def save_data(
    data,
    to_json: bool = False,
    to_csv: bool = False,
):
    """
    Save the given data to JSON and/or CSV files based on the arguments.

    :param data: The data to be saved, which can be a dict or a list of dicts.
    :param to_json: Used to get the True value and the filename for the created JSON file if specified.
    :param to_csv: Used to get the True value and the filename for the created CSV file if specified.
    """
    from .base import User, Subreddit

    if to_json or to_csv:
        if isinstance(data, (User, Subreddit)):
            function_data = data.__dict__
        elif isinstance(data, list):
            function_data = [item.__dict__ for item in data]
        else:
            log.error(
                f"Got an unexpected data type ({type(data)}), "
                f"expected {dict} or {list} of {dict}."
            )
            return

        if to_json:
            json_path = os.path.join(JSON_DIRECTORY, f"{to_json}.json")
            with open(json_path, "w", encoding="utf-8") as json_file:
                json.dump(function_data, json_file, indent=4)
            log.info(
                f"{os.path.getsize(json_file.name)} bytes written to {json_file.name}"
            )

        if to_csv:
            csv_path = os.path.join(CSV_DIRECTORY, f"{to_csv}.csv")
            with open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
                writer = csv.writer(csv_file)
                if isinstance(function_data, dict):
                    writer.writerow(function_data.keys())
                    writer.writerow(function_data.values())
                elif isinstance(function_data, list):
                    if function_data:
                        writer.writerow(
                            function_data[0].keys()
                        )  # header from keys of the first item
                        for item in function_data:
                            writer.writerow(item.values())
            log.info(
                f"{os.path.getsize(csv_file.name)} bytes written to {csv_file.name}"
            )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def setup_logging(debug_mode: bool) -> logging.getLogger:
    """
    Configure and return a logging object with the specified log level.

    :param debug_mode: A boolean value indicating whether log level should be set to DEBUG.
    :return: A logging object configured with the specified log level.
    """
    from rich.logging import RichHandler

    logging.basicConfig(
        level="DEBUG" if debug_mode else "INFO",
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
