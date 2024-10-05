import os
from types import SimpleNamespace
from typing import Union, Literal, List, Tuple, Dict

import pandas as pd

from .shared import notify

__all__ = [
    "create_dataframe",
    "export_dataframe",
    "plot_bar_chart",
    "EXPORT_FORMATS",
    "visualisation_dependency_installed",
]

EXPORT_FORMATS = Literal["csv", "html", "json", "xml"]

try:
    import matplotlib.pyplot as plt

    visualisation_dependency_installed: bool = True
except ImportError:
    visualisation_dependency_installed = False


def plot_bar_chart(
    data: Dict[str, int],
    title: str,
    xlabel: str,
    ylabel: str,
    colours: List[str],
    filename: str,
    figure_size: Tuple[int, int] = (10, 5),
):
    """
    Plots a bar chart for the given data.

    :param data: A dictionary where keys are the categories and values are the counts or frequencies.
    :type data: list[str, int]
    :param title: The title of the plot.
    :type title: str
    :param xlabel: The label for the x-axis.
    :type xlabel: str
    :param ylabel: The label for the y-axis.
    :type ylabel: str
    :param colours: A list of colours to use for the bars in the chart.
    :type colours: list[str]
    :param filename: The name of the file where the plot will be saved.
    :type filename: str
    :param figure_size: The size of the figure (width, height). Defaults to (10, 5).
    :type figure_size: tuple[int, int]
    """

    if visualisation_dependency_installed:
        plt.figure(figsize=figure_size)
        plt.bar(list(data.keys()), list(data.values()), color=colours)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.savefig(f"{filename}.png")

        notify.ok(f"{title} saved to [link file://{filename}.png]{filename}.png")


def create_dataframe(
    data: Union[SimpleNamespace, List[SimpleNamespace], List[Tuple[str, int]]],
) -> pd.DataFrame:
    """
    Makes a Pandas dataframe from the provided data.

    :param data: Data to be converted.
    :type data: Union[SimpleNamespace, List[SimpleNamespace], List[Tuple[str, int]]]
    :return: A pandas DataFrame constructed from the provided data. Excludes any 'raw_data'
             column from the dataframe.
    :rtype: pd.DataFrame
    """

    if isinstance(data, SimpleNamespace):
        # Transform each attribute of the object into a dictionary entry
        transformed_data = [
            {"key": key, "value": value} for key, value in data.__dict__.items()
        ]

    # Convert a list of SimpleNamespace objects to a list of dictionaries
    elif isinstance(data, List) and all(
        isinstance(item, SimpleNamespace) for item in data
    ):
        # Each object in the list is transformed to its dictionary representation
        transformed_data = [item.__dict__ for item in data]
    else:
        transformed_data = data

    # Set pandas display option to show all rows
    pd.set_option("display.max_rows", None)

    # Create a DataFrame from the transformed data
    dataframe = pd.DataFrame(transformed_data)

    return dataframe.dropna(axis=1, how="all")


def export_dataframe(
    dataframe: pd.DataFrame,
    filename: str,
    directory: str,
    formats: List[EXPORT_FORMATS],
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

    file_mapping: Dict = {
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
            notify.ok(
                f"{get_file_size(file_path=filepath)} written to [link file://{filepath}]{filepath}"
            )
        else:
            continue


def get_file_size(file_path: str) -> str:
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


# -------------------------------- END ----------------------------------------- #
