# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

import os
from datetime import datetime
from typing import Union, Literal

import pandas as pd
from rich.console import Console

from .data import Comment, Post, Community, User, PreviewCommunity, WikiPage


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


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def dataframe(
    data: Union[
        dict,
        list,
        list[Union[Comment, Community, Post, PreviewCommunity, User]],
        User,
        WikiPage,
        Community,
    ],
    export_to: list[Literal["csv", "html", "json", "xml"]] = None,
    export_dir: str = None,
):
    """
    Converts and prints provided data into a pandas DataFrame and optionally exports it to files.

    :param data: Data to be converted. Can be a single object (Community, User, WikiPage),
                 a dictionary, or a list of objects (Comment, Community, Post, PreviewCommunity, User).
    :type data: Union[Community, Dict, User, WikiPage, List[Union[Comment, Community, Post, PreviewCommunity, User]]]
    :param export_to: Optional. A list of file types to export the dataframe to.
    :type export_to: list[Literal]
    :param export_dir: Optional. Directory to which the exported dataframe files will be saved.
    :type export_dir: str
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

    # Export the data frane to files
    export_dataframe(
        df=df, filename=filename_timestamp(), directory=export_dir, formats=export_to
    )

    # Print the DataFrame, excluding the 'raw_data' column if it exists
    console.print(df.loc[:, df.columns != "raw_data"])


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def export_dataframe(
    df: pd.DataFrame,
    filename: str,
    directory: str,
    formats: list[Literal["csv", "html", "json", "xml"]],
):
    """
    Exports a Pandas dataframe to specified file formats.

    :param df: Pandas dataframe to export.
    :type df: pandas.DataFrame
    :param filename: Name of the file to which the dataframe will be exported.
    :type filename: str
    :param directory: Directory to which the dataframe files will be saved.
    :type directory: str
    :param formats: A list of file formats to which the data will be exported.
    :type formats: list[Literal]
    """
    file_mapping: dict = {
        "csv": lambda: df.to_csv(
            os.path.join(directory, "csv", f"{filename}.csv"), encoding="utf-8"
        ),
        "html": lambda: df.to_html(
            os.path.join(directory, "html", f"{filename}.html"),
            escape=False,
            encoding="utf-8",
        ),
        "json": lambda: df.to_json(
            os.path.join(directory, "json", f"{filename}.json"),
            encoding="utf-8",
            orient="records",
            lines=True,
            force_ascii=False,
            indent=4,
        ),
        "xml": lambda: df.to_xml(
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
                f"{os.path.getsize(filepath)} bytes written to [link file://{filepath}]{filepath}"
            )
        else:
            console.log(f"Unsupported file format: {file_format}")


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

console = Console(color_system="auto", log_time_format="[%I:%M:%S%p]")

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
