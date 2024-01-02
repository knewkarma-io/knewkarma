# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

import logging
import os
from datetime import datetime
from typing import Union

import pandas as pd

from ._parser import create_parser
from .data import Comment, Post, Community, User, PreviewCommunity, WikiPage


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def dataframe(
    data: Union[
        Community,
        User,
        WikiPage,
        dict,
        list,
        list[Union[Comment, Community, Post, PreviewCommunity, User]],
    ],
    to_dir: str,
    save_csv: str = None,
    save_json: str = None,
):
    """
    Converts and prints provided data into a pandas DataFrame and optionally saves it as JSON or CSV file.

    :param data: Data to be converted. Can be a single object (Community, User, WikiPage),
                 a dictionary, or a list of objects (Comment, Community, Post, PreviewCommunity, User).
    :type data: Union[Community, Dict, User, WikiPage, List[Union[Comment, Community, Post, PreviewCommunity, User]]]
    :param save_csv: Optional. If provided, saves the DataFrame as a CSV file. Can be a boolean
                     (True for default naming) or a string (specific file name).
    :type save_csv: str
    :param save_json: Optional. If provided, saves the DataFrame as a JSON file. Can be a boolean
                      (True for default naming) or a string (specific file name).
    :type save_json: str
    :param to_dir: Directory path where the JSON/CSV file, will be stored (if saved).
    :type to_dir: str
    :return: A pandas DataFrame constructed from the provided data. Excludes any 'raw_data'
             column from the dataframe.
    :rtype: pd.DataFrame

    Note
    ----
        This function internally converts User, Community, and WikiPage objects into a
        list of dictionaries before DataFrame creation.
        For lists containing Comment, Community, Post, PreviewCommunity and User objects,
        each object is converted to its dictionary representation.
    """
    from rich import print

    # Convert single User, Community, or WikiPage objects to a list of dictionaries
    if isinstance(data, (User, Community, WikiPage)):
        # Transform each attribute of the object into a dictionary entry
        data = [{"key": key, "value": value} for key, value in data.__dict__.items()]

    # Convert a list of objects (Comment, Community, Post, PreviewCommunity, User) to a list of dictionaries
    elif isinstance(data, list) and all(
        isinstance(item, (Comment, Community, Post, PreviewCommunity, User))
        for item in data
    ):
        # Each object in the list is converted to its dictionary representation
        data = [item.__dict__ for item in data]

    # If data is already a dictionary or a list, use it directly for DataFrame creation
    elif isinstance(data, (dict, list)):
        # No transformation needed; the data is ready for DataFrame creation
        pass

    # Set pandas display option to show all rows
    pd.set_option("display.max_rows", None)

    # Create a DataFrame from the processed data
    df = pd.DataFrame(data)

    # Save the DataFrame to CSV or JSON if specified
    save_dataframe(df=df, save_csv=save_csv, save_json=save_json, to_dir=to_dir)

    # Print the DataFrame, excluding the 'raw_data' column if it exists
    print(df.loc[:, df.columns != "raw_data"])


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def save_dataframe(
    df: pd.DataFrame,
    save_csv: str,
    save_json: str,
    to_dir: str,
):
    """
    Saves a pandas DataFrame to JSON and/or CSV files.

    :param df: The DataFrame to be saved.
    :type df: pandas.DataFrame
    :param save_csv: The base name for the CSV file. If provided, saves the DataFrame to a CSV file.
    :type save_csv: str
    :param save_json: The base name for the JSON file. If provided, saves the DataFrame to a JSON file.
    :type save_json: str
    :param to_dir: The directory where the files will be saved.
    :type to_dir: str
    """
    if save_csv:
        csv_filename = f"{save_csv.upper()}-{filename_timestamp()}.csv"
        csv_filepath = os.path.join(to_dir, "csv", csv_filename)
        df.to_csv(csv_filepath, index=False)
        log.info(
            f"{os.path.getsize(csv_filepath)} bytes written to [link file://{csv_filepath}]{csv_filepath}"
        )

    if save_json:
        json_filename = f"{save_json.upper()}-{filename_timestamp()}.json"
        json_filepath = os.path.join(to_dir, "json", json_filename)
        df.to_json(json_filepath, orient="records", lines=True, indent=4)
        log.info(
            f"{os.path.getsize(json_filepath)} bytes written to [link file://{json_filepath}]{json_filepath}"
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
                markup=True, log_time_format="[%I:%M:%S%p]", show_level=debug_mode
            )
        ],
    )
    return logging.getLogger("Knew Karma")


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

log: logging.getLogger = setup_logging(debug_mode=create_parser().parse_args().debug)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #