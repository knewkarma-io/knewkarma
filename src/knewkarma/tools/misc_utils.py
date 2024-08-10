import os
from typing import Union

from rich.box import DOUBLE
from rich.console import Console, ConsoleRenderable, RichCast
from rich.panel import Panel

from .styling_utils import Text

__all__ = ["console", "create_panel", "pathfinder"]


def create_panel(
    title: str,
    content: Union[ConsoleRenderable, RichCast, str],
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

        >>> from knewkarma.tools.misc_utils import create_panel

        >>> create_panel(
        >>>     title="Did you know?",
        >>>     content="The word 'bed' looks like a BED",
        >>>     subtitle="*sarcastic* oh wow!",
        >>>     )
    """
    console.print(
        Panel(
            renderable=content,
            title=f"{Text.bold}{title}{Text.reset}",
            subtitle=(subtitle if subtitle else None),
            expand=False,
            box=DOUBLE,
            style=f"{Text.white.strip('[,]')} on {Text.blue.strip('[,]')}",
        )
    )


def pathfinder(directories: list[str]):
    """
    Creates directories in src-output directory of the user's home folder.

    :param directories: A list of file directories to create.
    :type directories: list[str]
    """
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


console = Console(color_system="auto", log_time=False)

# -------------------------------- END ----------------------------------------- #
