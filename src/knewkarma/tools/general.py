import os
from typing import Union

from rich.box import DOUBLE
from rich.console import Console, ConsoleRenderable, RichCast
from rich.panel import Panel

__all__ = ["console", "make_panel", "pathfinder", "ML_MODELS_DIR", "OUTPUT_PARENT_DIR"]


def make_panel(
    title: str,
    content: Union[ConsoleRenderable, RichCast, str],
    subtitle: str = None,
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
    from .console import Colour

    colour = Colour
    console.print(
        Panel(
            renderable=content,
            title=f"{colour.bold}{title}{colour.reset}",
            subtitle=(subtitle if subtitle else None),
            expand=False,
            box=DOUBLE,
            style=f"{colour.white.strip('[,]')} on {colour.blue.strip('[,]')}",
        )
    )


def pathfinder(directories: Union[list[list[str]], str, None]):
    """
    Creates directories for exported data (`exported`) and
    Machine Learning models (`ml_models`) in knewkarma directory of the user's home folder.

    :param directories: A list of directories to create
    :type directories: list[str]
    :raise TypeError: If the data type of the specified directories is invalid.
    """
    from .console import Notify

    notify = Notify
    try:
        for directory in directories:
            if isinstance(directory, list):
                for child_dir in directory:
                    os.makedirs(child_dir, exist_ok=True)
            elif isinstance(directory, str):
                os.makedirs(directory, exist_ok=True)
            elif directory is None:
                pass
            else:
                notify.raise_exception(
                    TypeError,
                    f"Unexpected data type in the `directories` param: {type(directories)}. Expected list[list[str]] | str",
                )
    except Exception as unexpected_error:
        notify.exception(
            error=unexpected_error,
            exception_type="unexpected",
            exception_context="while creating directories",
        )


console = Console(log_time=False)

OUTPUT_PARENT_DIR: str = os.path.expanduser(os.path.join("~", "knewkarma"))
ML_MODELS_DIR: str = os.path.join(OUTPUT_PARENT_DIR, "ml_models")

# -------------------------------- END ----------------------------------------- #
