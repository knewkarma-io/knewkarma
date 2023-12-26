# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

import logging
import os
from datetime import datetime
from typing import Union, List, Dict

import pandas as pd

from ._parser import create_parser
from .data import Comment, Post, Community, User, PreviewCommunity


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def dataframe(
    data: Union[
        User,
        Community,
        Dict,
        List[Union[Post, Comment, Community, PreviewCommunity]],
    ],
    save_to_dir: str,
    save_json: Union[bool, str] = False,
    save_csv: Union[bool, str] = False,
) -> pd.DataFrame:
    """
    Creates a pandas DataFrame from various types of data and optionally save it to JSON or CSV.

    :param data: Data to be converted into a DataFrame. This can be a User, Community, dictionary,
                 or a list of Post, Comment, Community, or PreviewCommunity objects.
    :param save_to_dir: Directory path where the JSON/CSV file will be saved.
    :param save_json: If provided, the DataFrame will be saved as a JSON file. This can be a boolean or a string.
                      If it's a string, it will be used as the base name for the file.
    :param save_csv: If provided, the DataFrame will be saved as a CSV file. This can be a boolean or a string.
                     If it's a string, it will be used as the base name for the file.
    :return: A pandas DataFrame created from the provided data.
    """
    # Convert single User or Community objects to a list of dictionaries
    if isinstance(data, (User, Community)):
        data = [{"key": key, "value": value} for key, value in data.__dict__.items()]
    # Convert a list of User or Community objects
    elif isinstance(data, list) and all(
        isinstance(item, (User, Community)) for item in data
    ):
        data = [
            {"key": key, "value": value}
            for item in data
            for key, value in item.__dict__.items()
        ]
    # For other types of data, directly use it for DataFrame creation
    elif not isinstance(data, Dict):
        data = data

    pd.set_option("display.max_rows", None)
    df = pd.DataFrame(data)
    save_dataframe(
        df=df, save_csv=save_csv, save_json=save_json, save_to_dir=save_to_dir
    )

    return df.loc[:, df.columns != "raw_data"]  # Exclude 'raw_data' column if it exists


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def save_dataframe(
    df: pd.DataFrame,
    save_csv: str,
    save_json: str,
    save_to_dir: str,
):
    """
    Saves a pandas DataFrame to JSON and/or CSV files.

    :param df: The DataFrame to be saved.
    :type df: pandas.DataFrame
    :param save_csv: The base name for the CSV file. If provided, saves the DataFrame to a CSV file.
    :type save_csv: str
    :param save_json: The base name for the JSON file. If provided, saves the DataFrame to a JSON file.
    :type save_json: str
    :param save_to_dir: The directory where the files will be saved.
    :type save_to_dir: str
    """
    if save_csv:
        csv_filename = f"{save_csv.upper()}-{filename_timestamp()}.csv"
        csv_filepath = os.path.join(save_to_dir, "csv", csv_filename)
        df.to_csv(csv_filepath, index=False)
        log.info(
            f"{os.path.getsize(csv_filepath)} bytes written to [link file://{csv_filename}]{csv_filename}"
        )

    if save_json:
        json_filename = f"{save_json.upper()}-{filename_timestamp()}.json"
        json_filepath = os.path.join(save_to_dir, "json", json_filename)
        df.to_json(json_filepath, orient="records", lines=True, indent=4)
        log.info(
            f"{os.path.getsize(json_filepath)} bytes written to [link file://{json_filename}]{json_filename}"
        )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def filename_timestamp() -> str:
    """
    Generates a timestamp string suitable for file naming, based on the current date and time.
    The format of the timestamp is adapted based on the operating system.

    :return: The formatted timestamp as a string. The format is "%d-%B-%Y-%I-%M-%S%p" for Windows
             and "%d-%B-%Y-%I:%M:%S%p" for non-Windows systems.
    :rtype: str

    Example
    -------
    - Windows: "20-July-1969-08-17-45PM"
    - Non-Windows: "20-July-1969-08:17:45PM" (format may vary based on the current date and time)
    """
    now = datetime.now()
    return (
        now.strftime("%d-%B-%Y-%I-%M-%S%p")
        if os.name == "nt"
        else now.strftime("%d-%B-%Y-%I:%M:%S%p")
    )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def pathfinder(directories: list[str]):
    """
    Creates directories in knewkarma-data directory of the user's home folder.

    :param directories: A list of file directories to create.
    :type directories: list[str]
    """
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def unix_timestamp_to_utc(timestamp: int) -> str:
    """
    Converts a UNIX timestamp to a formatted datetime.utc string.

    :param timestamp: The UNIX timestamp to be converted.
    :type timestamp: int
    :return: A formatted datetime.utc string in the format "dd MMMM yyyy, hh:mm:ssAM/PM"
    :rtype: str
    """
    utc_from_timestamp: datetime = datetime.utcfromtimestamp(timestamp)
    datetime_string: str = utc_from_timestamp.strftime("%d %B %Y, %I:%M:%S%p")

    return datetime_string


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def setup_logging(debug_mode: bool) -> logging.getLogger:
    """
    Configure and return a logging object with the specified log level.

    :param debug_mode: A boolean value indicating whether log level should be set to DEBUG.
    :type debug_mode: bool
    :return: A logging object configured with the specified log level.
    :rtype: logging.getLogger
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


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

log: logging.getLogger = setup_logging(debug_mode=create_parser().parse_args().debug)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
