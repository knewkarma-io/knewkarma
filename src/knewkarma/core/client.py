from platform import python_version, platform

from engines.snoopy import reddit
from ..meta.about import Project
from ..meta.version import Version

USER_AGENT: str = (
    f"{Project.name.replace(' ', '-')}/{Version.release} "
    f"(Python {python_version} on {platform}; +{Project.documentation})"
)
reddit = reddit.Reddit(user_agent=USER_AGENT)
