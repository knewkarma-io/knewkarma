import os
from typing import Union, Text

from rich.box import DOUBLE
from rich.console import Console, ConsoleRenderable, RichCast
from rich.panel import Panel

__all__ = ["console", "create_panel", "pathfinder"]


def create_panel(
        title: str,
        content: Union[ConsoleRenderable, RichCast, Text],
        subtitle: str = None,
):
    """
    Creates a rich Panel for whatever data is needed to be placed in it.

    :param title: Panel title.
    :type title: str
    :param content: Content of the panel.
    :type content: Union[rich.ConsoleRenderable, rich.RichCast, str]
    :param subtitle: Panel subtitle.
    :type subtitle: str

    Usage::

        >>> from knewkarma.tools.general_utils import create_panel

        >>> create_panel(
        >>>     title="Did you know?",
        >>>     content="The word 'bed' looks like a BED",
        >>>     subtitle="*sarcastic* oh wow!",
        >>>     )
    """
    console.print(
        Panel(
            renderable=content,
            title=f"[bold]{title}[/]",
            subtitle=(subtitle if subtitle else None),
            style="white on black",
            expand=False,
            box=DOUBLE,
        )
    )


def pathfinder(directories: list[str]):
    """
    Creates directories in knewkarma-output directory of the user's home folder.

    :param directories: A list of file directories to create.
    :type directories: list[str]
    """
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


console = Console(color_system="auto", log_time=False)

# -------------------------------- END ----------------------------------------- #
