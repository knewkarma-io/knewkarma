import os
import subprocess
import typing as t
from datetime import datetime
from types import SimpleNamespace

import pandas as pd

from .logging import logger

__all__ = ["Data"]


class Data:

    EXPORT_FORMATS = t.Literal["csv", "html", "json", "xml"]
    EXPORTS_PARENT_DIR: str = os.path.expanduser(os.path.join("~", "knewkarma"))

    @classmethod
    def make_dataframe(
        cls,
        data: t.Union[
            SimpleNamespace, t.List[SimpleNamespace], t.List[t.Tuple[str, int]]
        ],
    ) -> pd.DataFrame:
        """
        Makes a Pandas dataframe from the provided data.

        :param data: Data to be converted.
        :type data: Union[SimpleNamespace, List[SimpleNamespace], List[Tuple[str, int]]]
        :return: A pandas DataFrame constructed from the provided data.
        :rtype: pd.DataFrame
        """
        if isinstance(data, SimpleNamespace):
            # Transform each attribute of the object into a dictionary entry
            transformed_data = [
                {"attribute": key, "value": value}
                for key, value in data.data.__dict__.items()
            ]

        # Convert a list of SimpleNamespace objects to a list of dictionaries
        elif isinstance(data, t.List) and all(
            isinstance(item, SimpleNamespace) for item in data
        ):
            # Each object in the list is transformed to its dictionary representation
            transformed_data = [item.data.__dict__ for item in data]
        else:
            transformed_data = data

        # Set pandas display option to show all rows
        pd.set_option("display.max_rows", None)

        # Create a DataFrame from the transformed data
        dataframe = pd.DataFrame(transformed_data)

        return dataframe.dropna(axis=1, how="all")

    @classmethod
    def export_dataframe(
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
                    f"{cls.get_file_size(file_path=filepath)} written to [link file://{filepath}]{filepath}"
                )
            else:
                continue

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

        return f"{file_size_bytes:.2f} {units[unit_index]}"

    @classmethod
    def filename_timestamp(cls) -> str:
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

    @classmethod
    def clear_screen(cls):
        subprocess.run(["cls" if os.name == "nt" else "clear"])


# -------------------------------- END ----------------------------------------- #
