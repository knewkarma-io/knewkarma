import logging

from rich.console import Console
from rich.logging import RichHandler

__all__ = ["console", "logger"]

console = Console(highlight=True)
logger = logging.getLogger("rich")

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[
        RichHandler(
            console=console,
            markup=True,
            show_time=False,
            show_level=False,
        )
    ],
)
