from platform import python_version, platform

from engines.snoopy import reddit
from ..meta.about import Project
from ..meta.version import Version

reddit = reddit.Reddit(
    user_agent=f"{Project.name.replace(' ', '-')}/{Version.release} "
    f"(Python {python_version} on {platform}; +{Project.documentation})"
)
