import os
from datetime import datetime
from typing import Union, List, Optional

from rich.box import DOUBLE
from rich.console import ConsoleRenderable, RichCast
from rich.panel import Panel

from .shared_utils import console, notify

__all__ = [
    "filename_timestamp",
    "make_panel",
    "pathfinder",
]


def make_panel(
        title: str,
        content: Union[ConsoleRenderable, RichCast, str],
        subtitle: Optional[str] = None,
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
    from .terminal_utils import Style

    console.print(
        Panel(
            renderable=content,
            title=f"{Style.bold}{title}{Style.reset}",
            subtitle=(subtitle if subtitle else None),
            box=DOUBLE,
            style=f"{Style.white.strip('[,]')} on black",
        )
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


def pathfinder(directories: Union[List[str], str]):
    """
    Creates directories for exported data (`exported`).

    :param directories: A list of directories or a directory name to create
    :type directories: Union[List[str], str]
    :raise Exception: If any was encountered.
    """

    try:
        if isinstance(directories, List) and all(
                isinstance(directory, str) for directory in directories
        ):
            for directory in directories:
                os.makedirs(name=directory, exist_ok=True)
        elif isinstance(directories, str):
            os.makedirs(name=directories, exist_ok=True)
    except Exception as unexpected_error:
        notify.exception(unexpected_error)

# -------------------------------- END ----------------------------------------- #
