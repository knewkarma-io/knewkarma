import os
import subprocess
import typing as t
from datetime import datetime
from types import SimpleNamespace

import pandas as pd
from rich import box
from rich.console import ConsoleRenderable, RichCast, Group
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

from . import colours
from .logging import console, logger

__all__ = ["DataAndVisualisation"]


class DataAndVisualisation:

    EXPORT_FORMATS = t.Literal["csv", "html", "json", "xml"]
    EXPORTS_PARENT_DIR: str = os.path.expanduser(os.path.join("~", "knewkarma"))

    @classmethod
    def plot_bar_chart(
        cls,
        data: t.Dict[str, int],
        title: str,
        x_label: str,
        y_label: str,
    ):
        """
        Renders a simple bar chart in the terminal using Rich.

        :param data: A dictionary of category-value pairs.
        :param title: Title of the chart.
        :param x_label: Label for the x-axis (shown in the subtitle).
        :param y_label: Label for the y-axis (shown in the subtitle).
        """

        max_value = max(data.values()) or 1  # Avoid divide-by-zero
        table = Table(show_header=False, box=None, expand=True)
        table.add_column("Category", justify="right")
        table.add_column("Bar", justify="left")

        for label, value in data.items():
            bar_length = int((value / max_value) * 40)
            bar = "█" * bar_length
            table.add_row(f"[bold]{label}[/bold]", f"{bar} {value}")

        subtitle = f"{x_label} vs {y_label}" if x_label and y_label else ""
        panel = Panel(
            table, title=f"[bold magenta]{title}[/bold magenta]", subtitle=subtitle
        )
        console.print(panel)

    @classmethod
    def print_table(
            cls,
            data: t.Union[SimpleNamespace, t.List[SimpleNamespace], t.List[t.Tuple[str, int]]],
            n_head: t.Optional[int] = None,
            n_tail: t.Optional[int] = None,
    ):
        """
        Creates and displays a rich-formatted table from the provided data.

        Any keys that contain only `None` values across all rows are excluded.
        Dynamically adjusts columns shown based on terminal width.

        :param data: Input data to display.
        :type data: Union[SimpleNamespace, List[SimpleNamespace], List[Tuple[str, int]]]
        :param n_head: Number of keys to show from the start (optional).
        :param n_tail: Number of keys to show from the end (optional).
        """
        terminal_width = console.size.width

        # Estimate how many columns we can show
        # Assume 15 chars per column (avg); minus some buffer for borders
        max_columns = max((terminal_width - 10) // 15, 1)

        # If user didn't specify n_head/n_tail, we balance them based on space
        if n_head is None or n_tail is None:
            half = max_columns // 2
            n_head = n_head or half
            n_tail = n_tail or (max_columns - n_head - 1)  # leave room for "..."

        table = Table(highlight=True, box=box.ASCII2, expand=True, show_lines=True)

        def extract_namespace(ns: SimpleNamespace) -> dict:
            if hasattr(ns, "data") and isinstance(ns.data, SimpleNamespace):
                return ns.data.__dict__
            return ns.__dict__

        # Case 1: Single SimpleNamespace
        if isinstance(data, SimpleNamespace):
            values = {k: v for k, v in extract_namespace(data).items() if v is not None}
            table.add_column("Key", style="cyan", no_wrap=True)
            table.add_column("Value", style="magenta")

            for key, value in values.items():
                table.add_row(str(key), str(value))

        # Case 2: List of SimpleNamespace
        elif isinstance(data, list) and all(isinstance(item, SimpleNamespace) for item in data):
            if not data:
                console.print("[bold red]Empty list provided.[/bold red]")
                return

            values_list = [extract_namespace(item) for item in data]

            non_none_keys = {
                key
                for d in values_list
                for key, value in d.items()
                if value is not None
            }

            if not non_none_keys:
                console.print("[bold yellow]All values were None. Nothing to show.[/bold yellow]")
                return

            all_keys = [k for k in values_list[0].keys() if k in non_none_keys]

            if len(all_keys) <= n_head + n_tail:
                visible_keys = all_keys
            else:
                visible_keys = all_keys[:n_head] + ["..."] + all_keys[-n_tail:]

            for key in visible_keys:
                table.add_column(key)

            for row_values in values_list:
                row = []
                for key in visible_keys:
                    if key == "...":
                        row.append("...")
                    else:
                        val = row_values.get(key)
                        row.append(str(val) if val is not None else "")
                table.add_row(*row)

        # Case 3: List of tuples
        elif isinstance(data, list) and all(isinstance(item, tuple) and len(item) == 2 for item in data):
            filtered = [(k, v) for k, v in data if v is not None]

            table.add_column("Key", style="cyan")
            table.add_column("Value", style="magenta")

            for key, value in filtered:
                table.add_row(str(key), str(value))

        console.print(table)

    @classmethod
    def create_dataframe(
        cls,
        data: t.Union[SimpleNamespace, t.List[SimpleNamespace], t.List[t.Tuple[str, int]]],
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
    def make_panel(
        cls,
        title: str,
        content: t.Union[ConsoleRenderable, RichCast, str],
        subtitle: t.Optional[str] = None,
    ):
        """
        Makes a rich Panel for whatever data is needed to be placed in it.

        :param title: Panel title.
        :type title: str
        :param content: Content of the panel.
        :type content: Union[rich.ConsoleRenderable, rich.RichCast, str]
        :param subtitle: Panel subtitle.
        :type subtitle: str
        """

        header = Text.from_markup(title, justify="center", overflow="ellipsis")
        divider = Rule(style=colours.WHITE.strip("[,]"))
        content_items = [header, divider, content]
        content = Group(*content_items)

        panel = Panel(renderable=content, title_align="left", subtitle=subtitle)

        console.print(panel)

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
