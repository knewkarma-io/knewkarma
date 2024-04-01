import getpass
import locale
import os
import platform
import time
from datetime import datetime, timezone
from typing import Union, Literal

import pandas as pd
from rich.console import Console
from rich.tree import Tree


def systeminfo():
    """Shows some basic system info"""
    return {
        "python": platform.python_version(),
        "username": getpass.getuser(),
        "system": f"{platform.node()} {platform.release()} ({platform.system()})",
    }


def pathfinder(directories: list[str]):
    """
    Creates directories in knewkarma-data directory of the user's home folder.

    :param directories: A list of file directories to create.
    :type directories: list[str]
    """
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


def _timestamp_to_datetime(timestamp: float) -> str:
    """
    Converts a unix timestamp to a localized datetime string based on the system's locale.

    :param timestamp: Unix timestamp to convert.
    :type timestamp: float
    :return: A localized datetime string from the converted timestamp.
    :rtype: str
    """
    # Set the locale to the user's system default
    locale.setlocale(locale.LC_TIME, "")

    # Convert timestamp to a timezone-aware datetime object in UTC
    utc_object = datetime.fromtimestamp(timestamp, timezone.utc)

    local_object = utc_object.astimezone()

    # Format the datetime object according to the locale's conventions
    return local_object.strftime("%x, %X")


def _time_since(timestamp: int) -> str:
    """
    Convert a Unix timestamp into a human-readable time difference.

    :param timestamp: A Unix timestamp.
    :type timestamp: int
    :return: A string representing the time difference from now.
    :rtype: str
    """
    # Convert the current time to a Unix timestamp
    now = int(time.time())

    # Calculate the difference in seconds
    diff = now - timestamp

    # Define the time thresholds in seconds
    minute = 60
    hour = 60 * minute
    day = 24 * hour
    week = 7 * day
    month = 30 * day
    year = 12 * month

    # Determine the time unit and value
    if diff < minute:
        count = diff
        label = "seconds" if int(count) > 1 else "second"  # seconds
    elif diff < hour:
        count = diff // minute
        label = "minutes" if int(count) > 1 else "minute"  # minutes
    elif diff < day:
        count = diff // hour
        label = "hours" if int(count) > 1 else "hour"  # hours
    elif diff < week:
        count = diff // day
        label = "days" if int(count) > 1 else "day"
    elif diff < month:
        count = diff // week
        label = "weeks" if int(count) > 1 else "week"
    elif diff < year:
        count = diff // month
        label = "months" if int(count) > 1 else "month"
    else:
        count = diff // year
        label = "years" if int(count) > 1 else "year"

    return "just now" if int(count) == 0 else f"{int(count)} {label} ago"


def timestamp_to_readable(
    timestamp: float, time_format: Literal["concise", "datetime"] = "datetime"
) -> str:
    """
    Converts a Unix timestamp into a more readable format based on the specified `time_format`.
    The function supports converting the timestamp into either a localized datetime string or a concise
    human-readable time difference (e.g., "3 hours ago").

    :param timestamp: The Unix timestamp to be converted.
    :type timestamp: float
    :param time_format: Determines the format of the output time. Use "concise" for a human-readable
                        time difference, or "datetime" for a localized datetime string. Defaults to "datetime".
    :type time_format: Literal["concise", "datetime"]
    :return: A string representing the formatted time. The format is determined by the `time_format` parameter.
    :rtype: str
    :raises ValueError: If `time_format` is not one of the expected values ("concise" or "datetime").
    """
    if time_format == "concise":
        return _time_since(timestamp=int(timestamp))
    elif time_format == "datetime":
        return _timestamp_to_datetime(timestamp=timestamp)
    else:
        raise ValueError(
            f"Unknown time format {time_format}. Expected `concise` or `datetime`."
        )


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
    - Non-Windows: "20-July-1969-08:17:45PM"
    """
    now = datetime.now()
    return (
        now.strftime("%d-%B-%Y-%I-%M-%S%p")
        if os.name == "nt"
        else now.strftime("%d-%B-%Y-%I:%M:%S%p")
    )


def create_dataframe(
    data: Union[dict, list[dict], list[tuple]],
):
    """
    Converts provided data into a pandas DataFrame.

    :param data: Data to be converted.
    :type data: Union[dict, list[dict], list[str]]
    :return: A pandas DataFrame constructed from the provided data. Excludes any 'raw_data'
             column from the dataframe.
    :rtype: pd.DataFrame
    """

    if isinstance(data, dict):
        # Transform each attribute of the object into a dictionary entry
        data = [{"key": key, "value": value} for key, value in data.items()]

    # Convert a list of objects (Comment, Community, Post, PreviewCommunity, User) to a list of dictionaries
    elif isinstance(data, list) and all(
        isinstance(item, (dict, tuple)) for item in data
    ):
        # Each object in the list is converted to its dictionary representation
        data = [item for item in data]

    # Set pandas display option to show all rows
    pd.set_option("display.max_rows", None)

    # Create a DataFrame from the processed data
    dataframe = pd.DataFrame(data)

    return dataframe


def show_exported_files(tree: Tree, directory: str, base_path: str = ""):
    for item in sorted(os.listdir(directory)):
        path = os.path.join(directory, item)
        if os.path.isdir(path):
            branch = tree.add(f":open_file_folder: {item}", guide_style="blue")
            show_exported_files(branch, path, os.path.join(base_path, item))
        else:
            filepath: str = os.path.join(directory, path, item, path)
            tree.add(f":page_facing_up: [italic][link file://{filepath}]{item}[/]")


def export_dataframe(
    dataframe: pd.DataFrame,
    filename: str,
    directory: str,
    formats: list[Literal["csv", "html", "json", "xml"]],
):
    """
    Exports a Pandas dataframe to specified file formats.

    :param dataframe: Pandas dataframe to export.
    :type dataframe: pandas.DataFrame
    :param filename: Name of the file to which the dataframe will be exported.
    :type filename: str
    :param directory: Directory to which the dataframe files will be saved.
    :type directory: str
    :param formats: A list of file formats to which the data will be exported.
    :type formats: list[Literal]
    """
    file_mapping: dict = {
        "csv": lambda: dataframe.to_csv(
            os.path.join(directory, "csv", f"{filename}.csv"), encoding="utf-8"
        ),
        "html": lambda: dataframe.to_html(
            os.path.join(directory, "html", f"{filename}.html"),
            escape=False,
            encoding="utf-8",
        ),
        "json": lambda: dataframe.to_json(
            os.path.join(directory, "json", f"{filename}.json"),
            orient="records",
            lines=True,
            force_ascii=False,
            indent=4,
        ),
        "xml": lambda: dataframe.to_xml(
            os.path.join(directory, "xml", f"{filename}.xml"),
            parser="etree",
            encoding="utf-8",
        ),
    }

    for file_format in formats:
        if file_format in file_mapping:
            filepath: str = os.path.join(
                directory, file_format, f"{filename}.{file_format}"
            )
            file_mapping.get(file_format)()
            console.log(
                f"[green]✔[/] {os.path.getsize(filepath)} bytes written to [link file://{filepath}]{filepath}"
            )
        else:
            console.log(f"Unsupported file format: {file_format}")


console = Console(color_system="auto", log_time=False)
