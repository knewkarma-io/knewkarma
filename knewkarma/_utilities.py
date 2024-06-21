import asyncio
import locale
import os
from datetime import datetime, timezone
from typing import Union, Literal

import pandas as pd
from rich.console import Console
from rich.status import Status
from rich.table import Table
from rich.tree import Tree


def print_banner():
    """
    Prints the projects banner and system information.
    """
    console.log(
        f"""
┓┏┓         ┓┏┓
┃┫ ┏┓┏┓┓┏┏  ┃┫ ┏┓┏┓┏┳┓┏┓
┛┗┛┛┗┗ ┗┻┛  ┛┗┛┗┻┛ ┛┗┗┗┻"""
    )
    system_info()


def system_info():
    """
    Displays system information in a table format.
    """
    import getpass
    import platform
    import sys

    import psutil

    from .version import Version

    table = Table(show_header=False, show_edge=False, highlight=True)
    table.add_column("header", style="dim")
    table.add_column("header")

    # https://www.geeksforgeeks.org/getting-the-time-since-os-startup-using-python/
    if os.name == "nt":
        # ctypes required for using GetTickCount64()
        import ctypes

        # getting the library in which GetTickCount64() resides
        lib = ctypes.windll.kernel32

        # calling the function and storing the return value
        t = lib.GetTickCount64()

        # since the time is in milliseconds i.e. 1000 * seconds
        # therefore truncating the value
        t = int(str(t)[:-3])

        # extracting hours, minutes, seconds & days from t
        # variable (which stores total time in seconds)
        minutes, seconds = divmod(t, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        system_uptime = (
            "just now"
            if days == hours == minutes == seconds == 0
            else f"{days} days, {hours:02} hours, {minutes:02} minutes, and {seconds:02} seconds since boot"
        )
    else:
        system_uptime = _time_since(
            timestamp=int(psutil.boot_time()), suffix="since boot"
        )

    table.add_row("Knew Karma", Version.full)
    table.add_row("Python", sys.version)
    table.add_row("Username", getpass.getuser())
    table.add_row("System", f"{platform.system()} {platform.version()}")
    table.add_row(
        "CPU", f"{psutil.cpu_count(logical=True)} cores, {platform.processor()}"
    )
    table.add_row(
        "Disk",
        f"{psutil.disk_usage('/').free / (1024**3):.2f} GB free"
        f" / {psutil.disk_usage('/').total / (1024**3):.2f} GB",
    )
    table.add_row(
        "Memory",
        f"{psutil.virtual_memory().available / (1024**3):.2f} GB free"
        f" / {psutil.virtual_memory().total / (1024**3):.2f} GB",
    )

    table.add_row(
        "Uptime",
        system_uptime,
    )
    console.print(table)


def get_status(status_message: str) -> Status:
    """
    Creates and returns a Status object initialized with a specific status message.

    :param status_message: A message to initialise the Status with.
    :type status_message: str
    :return: A configured rich.status.Status object ready to be used in a context manager.
    :rtype: rich.status.Status
    """
    with Status(status=status_message, spinner="dots2", console=console) as status:
        return status


async def countdown_timer(
    status: Status, duration: int, current_count: int, limit: int
):
    """
    Handles the countdown during the asynchronous pagination, updating the status bar with the remaining time.

    :param status: The rich.status.Status object used to display the countdown.
    :type status: rich.status.Status
    :param duration: The duration for which to run the countdown.
    :type duration: int
    :param current_count: Current number of items fetched.
    :type current_count: int
    :param limit: Total number of items to fetch.
    :type limit: int
    """
    for remaining in range(duration, 0, -1):
        status.update(
            f"[cyan]{current_count}[/] of [cyan]{limit}[/] "
            f"items fetched so far. Resuming in [cyan]{remaining}[/]"
            f" {'second' if remaining <= 1 else 'seconds'}[yellow]...[/]"
        )
        await asyncio.sleep(1)  # Sleep for one second as part of countdown


def _timestamp_to_locale(timestamp: float) -> str:
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


def _time_since(timestamp: int, suffix: str = "ago") -> str:
    """
    Convert a Unix timestamp into a human-readable time difference.

    :param timestamp: A Unix timestamp.
    :type timestamp: int
    :return: A string representing the time difference from now.
    :rtype: str
    """
    import time

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

    return "just now" if int(count) == 0 else f"{int(count)} {label} {suffix}"


def timestamp_to_readable(
    timestamp: float, time_format: Literal["concise", "locale"] = "locale"
) -> str:
    """
    Converts a Unix timestamp into a more readable format based on the specified `time_format`.
    The function supports converting the timestamp into either a localized datetime string or a concise
    human-readable time difference (e.g., "3 hours ago").

    :param timestamp: The Unix timestamp to be converted.
    :type timestamp: float
    :param time_format: Determines the format of the output time. Use "concise" for a human-readable
                        time difference, or "locale" for a localized datetime string. Defaults to "locale".
    :type time_format: Literal["concise", "locale"]
    :return: A string representing the formatted time. The format is determined by the `time_format` parameter.
    :rtype: str
    :raises ValueError: If `time_format` is not one of the expected values ("concise" or "locale").
    """
    if time_format == "concise":
        return _time_since(timestamp=int(timestamp))
    elif time_format == "locale":
        return _timestamp_to_locale(timestamp=timestamp)
    else:
        raise ValueError(
            f"Unknown time format {time_format}. Expected `concise` or `locale`."
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


def pathfinder(directories: list[str]):
    """
    Creates directories in knewkarma-output directory of the user's home folder.

    :param directories: A list of file directories to create.
    :type directories: list[str]
    """
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


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
