import os
from sys import version as python_version

from rich.console import Console

from .api import Api, SORT_CRITERION, TIMEFRAME, TIME_FORMAT
from .meta import about, version
from .tools.terminal_utils import Notify, Style

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
        f"(Python {python_version}; +{about.documentation})"
    },
)

console = Console(log_time=False)

notify = Notify
style = Style

OUTPUT_PARENT_DIR: str = os.path.expanduser(os.path.join("~", "knewkarma"))
ML_MODELS_DIR: str = os.path.join(OUTPUT_PARENT_DIR, "ml_models")
