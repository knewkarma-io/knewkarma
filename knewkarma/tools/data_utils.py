import os
from typing import Union, Literal

import pandas as pd
from rich.tree import Tree

from .general_utils import console

__all__ = ["create_dataframe", "export_dataframe", "show_exported_files"]


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

    return dataframe.dropna(axis=1, how="all")


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
