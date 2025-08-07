import typing as t
from platform import platform, python_version

import praw

from karmakrate.handlers.auth_handler import AuthHandler
from ..meta.about import Project
from ..meta.version import Version

USER_AGENT: str = (
    f"{Project.name.replace(' ', '-')}/{Version.release} "
    f"(Python {python_version} on {platform}; +{Project.documentation})"
)
LISTINGS = t.Literal["controversial", "gilded", "hot", "new", "rising", "top"]
TIME_FILTERS = t.Literal["all", "hour", "day", "week", "month", "year"]
SORT = t.Literal["relevance", "hot", "top", "new", "lucene", "all"]

reddit = praw.Reddit(
    client_id=AuthHandler.read()["client_id"],
    client_secret=AuthHandler.read()["client_secret"],
    user_agent=USER_AGENT,
)
