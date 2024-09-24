import os
from platform import python_version, platform

from rich.console import Console

from .terminal_utils import Notify, Style
from ..api import Api, SORT_CRITERION, TIMEFRAME, TIME_FORMAT
from ..meta import about, version

__all__ = [
    "api",
    "console",
    "OUTPUT_PARENT_DIR",
    "ML_MODELS_DIR",
    "notify",
    "style",
    "SORT_CRITERION",
    "TIMEFRAME",
    "TIME_FORMAT",
]

api = Api(
    headers={
        "User-Agent": f"{about.name.replace(' ', '-')}/{version.release} "
                      f"(Python {python_version} on {platform}; +{about.documentation})"
    },
)

console = Console(log_time=False)

notify = Notify(console=console)
style = Style

OUTPUT_PARENT_DIR: str = os.path.expanduser(os.path.join("~", "knewkarma"))
ML_MODELS_DIR: str = os.path.join(OUTPUT_PARENT_DIR, "ml_models")
