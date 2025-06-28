import json
import os
import typing as t
from datetime import datetime

import pandas as pd
from praw.models import Submission, Redditor, Comment
from praw.models.reddit.subreddit import WikiPage, Subreddit
from rich.status import Status

from ..riches.rich_logging import console

__all__ = ["FileHandler", "DataFrameHandler"]


class DataFrameHandler:
    EXPORT_FORMATS = t.Literal["csv", "html", "json", "xml"]

    @classmethod
    def build(
        cls,
        data: t.Union[
            Redditor,
            Subreddit,
            Submission,
            WikiPage,
            Comment,
            t.List[t.Union[Redditor, Subreddit, Submission, WikiPage, Comment]],
            t.List[t.Tuple[str, t.Any]],
        ],
        status: Status,
    ) -> pd.DataFrame:

        if isinstance(status, Status):
            status.update("Loading data into a DataFrame dataframe...")

        def praw_to_dict(obj: t.Any) -> dict:
            """
            Converts a PRAW object to a dictionary by inspecting its __dict__.
            Filters out private/internal attributes.
            """
            raw = vars(obj)
            clean = {k: v for k, v in raw.items() if not k.startswith("_")}
            return clean

        # Handle a single PRAW object
        if hasattr(data, "__dict__") and not isinstance(data, list):
            transformed_data = [praw_to_dict(data)]

        # Handle list of PRAW objects
        elif isinstance(data, list) and all(hasattr(item, "__dict__") for item in data):
            transformed_data = [praw_to_dict(item) for item in data]

        # Handle list of (key, value) tuples
        elif isinstance(data, list) and all(
            isinstance(item, tuple) and len(item) == 2 for item in data
        ):
            transformed_data = [{key: value for key, value in data}]

        else:
            raise ValueError(f"Unsupported data type: {type(data)}")

        # Optional: display all rows when debugging
        pd.set_option("display.max_rows", None)

        # Build DataFrame, drop all-null columns
        df = pd.DataFrame(transformed_data)
        return df.dropna(axis=1, how="all")

    @classmethod
    def export(
        cls,
        dataframe: pd.DataFrame,
        filename: str,
        directory: str,
        formats: t.List[EXPORT_FORMATS],
        status: Status,
    ):
        """
        Exports a pandas DataFrame to one or more file formats, saving the output files to the specified directory.

        This method includes preprocessing specifically for XML export to ensure that all values in the
        DataFrame are scalar values (e.g., strings, integers, floats, or None), avoiding issues with
        non-scalar types such as lists or dictionaries.

        :param dataframe: The pandas DataFrame to export.
        :type dataframe: pd.DataFrame
        :param filename: The base name of the file (without extension) to save the exported data as.
        :type filename: str
        :param directory: The root directory under which subdirectories for each format (e.g., "csv", "xml") will be used.
        :type directory: str
        :param formats: A list of output formats to export the data to. Must be one or more of ["csv", "html", "json", "xml"].
        :type formats: List[Literal["csv", "html", "json", "xml"]]
        """

        if isinstance(status, Status):
            status.update(f"Exporting data to {formats}...")

        def sanitize_for_xml(df: pd.DataFrame) -> pd.DataFrame:
            """
            Converts all non-scalar values in the DataFrame to strings.

            This avoids pandas XML export errors by ensuring that each DataFrame cell contains a scalar value.

            :param df: The DataFrame to sanitize.
            :type df: pd.DataFrame
            :return: A sanitized DataFrame with all non-scalar values converted to strings.
            :rtype: pd.DataFrame
            """

            def scalarize(value: t.Any) -> t.Any:
                if isinstance(value, (list, dict, set)):
                    return json.dumps(value)
                return value

            return df.apply(lambda col: col.map(scalarize))

        # Preprocess DataFrame for XML if needed
        if "xml" in formats:
            dataframe = sanitize_for_xml(dataframe)

        file_mapping: t.Dict[str, t.Callable[[], None]] = {
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

                # Execute the export function for the current format
                file_mapping[file_format]()

                # Log export status
                console.log(
                    f"{FileHandler.get_file_size(file_path=filepath)} written to [link file://{filepath}]{filepath}"
                )


class FileHandler:
    PARENT_DIR: str = os.path.expanduser(os.path.join("~", "knewkarma"))
    AUTH_DIR: str = os.path.join(PARENT_DIR, "auth")

    @classmethod
    def get_file_size(cls, file_path: str) -> str:
        """
        Gets a file size and puts it in human-readable form.

        :param file_path: Path to target file.
        :type file_path: str
        :return: A human-readable form of the file size.
        :rtype: str
        """

        file_size_bytes: int = os.path.getsize(file_path)
        units: list = ["B", "KB", "MB", "GB", "TB", "PB"]

        unit_index: int = 0

        while file_size_bytes >= 1024 and unit_index < len(units) - 1:
            file_size_bytes /= 1024
            unit_index += 1

        return f"{file_size_bytes:.2f}{units[unit_index]}"

    @classmethod
    def time_to_filename(cls) -> str:
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

    @classmethod
    def pathfinder(cls, directories: t.Union[t.List[str], str]):
        """
        Creates directories for exported data (`exported`).

        :param directories: A list of directories or a directory name to create
        :type directories: Union[List[str], str]
        :raise Exception: If any was encountered.
        """

        try:
            if isinstance(directories, t.List) and all(
                isinstance(directory, str) for directory in directories
            ):
                for directory in directories:
                    os.makedirs(name=directory, exist_ok=True)
            elif isinstance(directories, str):
                os.makedirs(name=directories, exist_ok=True)
        except Exception as unexpected_error:
            console.log(unexpected_error)


# -------------------------------- END ----------------------------------------- #
