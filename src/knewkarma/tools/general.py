import asyncio
import os
import time
from datetime import datetime
from typing import Union, List, Optional

from rich.box import DOUBLE
from rich.console import Console, ConsoleRenderable, RichCast
from rich.panel import Panel
from rich.status import Status

__all__ = [
    "console",
    "countdown_timer",
    "filename_timestamp",
    "make_panel",
    "pathfinder",
    "ML_MODELS_DIR",
    "OUTPUT_PARENT_DIR",
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
    from .terminal import Style

    console.print(
        Panel(
            renderable=content,
            title=f"{Style.bold}{title}{Style.reset}",
            subtitle=(subtitle if subtitle else None),
            box=DOUBLE,
            style=f"{Style.white.strip('[,]')} on black",
        )
    )


async def countdown_timer(
    status: Status, duration: int, current_count: int, overall_count: int
):
    """
    Handles the live countdown during pagination, updating the status bar with the remaining time.

    :param status: A Status object used to display the countdown.
    :type status: rich.status.Status
    :param duration: The duration for which to run the countdown.
    :type duration: int
    :param current_count: Current number of items fetched.
    :type current_count: int
    :param overall_count: Overall number of items to fetch.
    :type overall_count: int
    """
    from .terminal import Notify, Style

    end_time: float = time.time() + duration
    while time.time() < end_time:
        remaining_time: float = end_time - time.time()
        remaining_seconds: int = int(remaining_time)
        remaining_milliseconds: int = int((remaining_time - remaining_seconds) * 100)

        Notify.update_status(
            message=f"{Style.cyan}{current_count}{Style.reset} (of {Style.cyan}{overall_count}{Style.reset}) items retrieved so far. "
            f"Resuming in {Style.cyan}{remaining_seconds}.{remaining_milliseconds:02}{Style.reset} seconds",
            status=status,
        )
        await asyncio.sleep(0.01)  # Sleep for 10 milliseconds


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


def pathfinder(directories: Union[List[List[str]], str, None]):
    """
    Creates directories for exported data (`exported`) and
    Machine Learning models (`ml_models`) in knewkarma directory of the user's home folder.

    :param directories: A list of directories to create
    :type directories: List[str]
    :raise TypeError: If the data type of the specified directories is invalid.
    """

    from .terminal import Notify

    try:
        for directory in directories:
            if isinstance(directory, List):
                for child_dir in directory:
                    os.makedirs(child_dir, exist_ok=True)
            elif isinstance(directory, str):
                os.makedirs(directory, exist_ok=True)
            else:
                pass
    except Exception as unexpected_error:
        Notify.exception(
            error=unexpected_error,
            exception_type="unexpected",
            exception_context="while creating directories",
        )


console = Console(log_time=False)

OUTPUT_PARENT_DIR: str = os.path.expanduser(os.path.join("~", "knewkarma"))
ML_MODELS_DIR: str = os.path.join(OUTPUT_PARENT_DIR, "ml_models")

# -------------------------------- END ----------------------------------------- #
