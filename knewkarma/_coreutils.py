# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

import csv
import json
import logging
import os
from typing import Union, List

from ._parser import create_parser
from .data import Comment, Post, Subreddit, User


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def timestamp_to_utc(timestamp: int) -> str:
    """
    Converts a UNIX timestamp to a formatted datetime.utc string.

    :param timestamp: The UNIX timestamp to be converted.
    :return: A formatted datetime.utc string in the format "dd MMMM yyyy, hh:mm:ssAM/PM"
    """
    from datetime import datetime

    utc_from_timestamp: datetime = datetime.utcfromtimestamp(timestamp)
    datetime_string: str = utc_from_timestamp.strftime("%d %B %Y, %I:%M:%S%p")

    return datetime_string


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def pathfinder(directories: list[str]):
    """
    Creates directories in knewkarma-data directory of the user's home folder.

    :param directories: A list of file directories to create.
    """
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def save_data(
    data: Union[User, Subreddit, List[Union[Post, Comment]]],
    save_to_dir: str,
    save_json: bool = False,
    save_csv: bool = False,
):
    """
    Save the given (Reddit) data to a JSON/CSV file based on the save_csv and save_json parameters.

    :param data: The data to be saved, which can be a dict or a list of dicts.
    :param save_to_dir: Directory to save data to.
    :param save_json: Used to get the True value and the filename for the created JSON file if specified.
    :param save_csv: Used to get the True value and the filename for the created CSV file if specified.
    """
    # -------------------------------------------------------------------- #

    if isinstance(data, (User, Subreddit)):
        function_data = data.__dict__
    elif isinstance(data, list):
        function_data = [item.__dict__ for item in data]
    else:
        log.critical(
            f"Got an unexpected data type ({type(data)}), "
            f"expected {type(User)}, {type(Subreddit)} or {List[Union[type(Post), type(Comment)]]}."
        )
        return

    # -------------------------------------------------------------------- #

    if save_json:
        json_path = os.path.join(save_to_dir, "json", f"{save_json}.json")
        with open(json_path, "w", encoding="utf-8") as json_file:
            json.dump(function_data, json_file, indent=4)
        log.info(
            f"{os.path.getsize(json_file.name)} bytes written to [link file://{json_file.name}]{json_file.name}"
        )

    # -------------------------------------------------------------------- #

    if save_csv:
        csv_path = os.path.join(save_to_dir, "csv", f"{save_csv}.csv")
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
            f"{os.path.getsize(csv_file.name)} bytes written to [link file://{csv_file.name}]{csv_file.name}"
        )


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


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


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

log: logging.getLogger = setup_logging(debug_mode=create_parser().parse_args().debug)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
