import os
import typing as t
from datetime import datetime

import pandas as pd

from engines.karmakaze.schemas import User, Subreddit, Post, WikiPage, Comment
from .log_config import logger

__all__ = ["FileHandler", "DataFrameHandler"]


class DataFrameHandler:
    EXPORT_FORMATS = t.Literal["csv", "html", "json", "xml"]

    @classmethod
    def build(
        cls,
        data: t.Union[
            User,
            Subreddit,
            Post,
            WikiPage,
            Comment,
            t.List[t.Union[User, Subreddit, Post, WikiPage, Comment]],
            t.List[t.Tuple[str, t.Any]],
        ],
    ) -> pd.DataFrame:
        """
        Makes a Pandas DataFrame from Pydantic model data.

        :param data: Data to be converted into a DataFrame. Can be a single Pydantic model,
                     a list of Pydantic models, or a list of (key, value) tuples.
        :return: A pandas DataFrame constructed from the provided data.
        """

        def to_dict(obj: t.Any) -> dict:
            """
            Converts a Pydantic v2 model to a dictionary using model_dump().
            """
            if hasattr(obj, "model_dump") and callable(obj.model_dump):
                return obj.model_dump()
            raise ValueError(f"Unsupported object type: {type(obj)}")

        # Handle a single Pydantic object
        if hasattr(data, "model_dump") and callable(data.model_dump):
            transformed_data = [to_dict(data)]

        # Handle a list of Pydantic objects
        elif isinstance(data, list) and all(
            hasattr(item, "model_dump") and callable(item.model_dump) for item in data
        ):
            transformed_data = [to_dict(item) for item in data]

        # Handle a list of (key, value) tuples
        elif isinstance(data, list) and all(
            isinstance(item, tuple) and len(item) == 2 for item in data
        ):
            transformed_data = [{key: value for key, value in data}]

        else:
            raise ValueError("Unsupported data structure for DataFrame conversion.")

        # Set display option for better debugging (optional)
        pd.set_option("display.max_rows", None)

        # Convert to DataFrame and clean it
        dataframe = pd.DataFrame(transformed_data)
        return dataframe.dropna(axis=1, how="all")

    @classmethod
    def export(
        cls,
        dataframe: pd.DataFrame,
        filename: str,
        directory: str,
        formats: t.List[EXPORT_FORMATS],
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
        :type formats: List[Literal]
        """

        file_mapping: t.Dict = {
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
                file_mapping.get(file_format)()
                logger.info(
                    f"{FileHandler.get_file_size(file_path=filepath)} written to [link file://{filepath}]{filepath}"
                )
            else:
                continue


class FileHandler:
    EXPORTS_PARENT_DIR: str = os.path.expanduser(os.path.join("~", "knewkarma"))

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
            logger.exception(unexpected_error)


# -------------------------------- END ----------------------------------------- #
