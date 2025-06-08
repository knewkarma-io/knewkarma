import os
import subprocess
import typing as t
from logging import Logger

import requests
from rich.status import Status

from engines.snoopy import Reddit
from knewkarma.meta.version import Version
from . import colours

__all__ = ["RuntimeOps"]


class RuntimeOps:
    """
    Provides utilities that are executed during the application's runtime.

    :param package_name:  The name of the package being inspected (used for update checks).
    :param reddit_cls: A class that implements request handling for Reddit-related endpoints.
    :param version_cls: A class that provides semantic version information
                                     (e.g., major, minor, patch versions).
    """

    def __init__(
        self, package_name: str, reddit_cls: Reddit, version_cls: t.Type[Version]
    ):
        self.package_name = package_name
        self.version_cls = version_cls
        self.reddit_cls = reddit_cls

    @classmethod
    def clear_screen(cls):
        subprocess.run(["cls" if os.name == "nt" else "clear"])

    def infra_status(
        self,
        session: requests.Session,
        logger: t.Optional[Logger] = None,
        status: t.Optional[Status] = None,
    ) -> t.Union[t.List[t.Dict], None]:

        if isinstance(status, Status):
            status.update(f"Checking server status...")

        status_response: dict = self.reddit_cls.send_request(
            url=self.reddit_cls.ENDPOINTS["infrastructure"]["status"],
            session=session,
            status=status,
            logger=logger,
        )

        indicator = status_response.get("status").get("indicator")
        description = status_response.get("status").get("description")
        if description:
            if indicator == "none":
                description = (
                    f"{colours.BOLD_GREEN}✔{colours.BOLD_GREEN_RESET} {description}"
                )
                (
                    logger.info(description)
                    if isinstance(logger, Logger)
                    else print(description.strip("[,]./,bold,green"))
                )
            else:
                status_message = f"{colours.BOLD_YELLOW}✘{colours.BOLD_YELLOW_RESET} {description} ({colours.YELLOW}{indicator}{colours.YELLOW_RESET})"
                (
                    logger.warning(status_message)
                    if isinstance(logger, Logger)
                    else print(status_message.strip("[,],/,bold,yellow"))
                )

                if isinstance(status, Status):
                    status.update("Getting status components...")

                status_components: t.Dict = self.reddit_cls.send_request(
                    url=self.reddit_cls.ENDPOINTS["infrastructure"]["components"],
                    session=session,
                    logger=logger,
                    status=status,
                )

                if isinstance(status_components, t.Dict):
                    components: t.List[t.Dict] = status_components.get("components")

                    return components
        return None

    def check_updates(
        self,
        session: requests.Session,
        status: t.Optional[Status] = None,
    ):
        """
        Asynchronously checks for updates by comparing the current local version with the remote version.

        Assumes version format: major.minor.patch.prefix

        :param session: An `requests.Session` for making the HTTP request.
        :type session: requests.Session
        :param status: An optional `Status` object for displaying status messages.
        :type status: t.Optional[rich.status.Status]
        """
        from .log_config import logger

        if isinstance(status, Status):
            status.update("Checking for updates")

        # Make a GET request to GitHub to get the project's latest release.
        response = self.reddit_cls.send_request(
            url=f"https://api.github.com/repos/knewkarma-io/{self.package_name}/releases/latest",
            session=session,
            logger=logger,
            status=status,
        )

        if response.get("tag_name"):
            remote_version_str = response.get("tag_name")

            # Splitting the version strings into components
            local_version_parts = [
                self.version_cls.major[0],
                self.version_cls.minor[0],
                self.version_cls.patch[0],
            ]
            remote_version_parts: t.List = remote_version_str.split(".")

            local_major: int = local_version_parts[0]
            local_minor: int = local_version_parts[1]
            local_patch: int = local_version_parts[2]

            remote_major = int(remote_version_parts[0])
            remote_minor = int(remote_version_parts[1])
            remote_patch = int(remote_version_parts[2])

            update_level = ""

            # Check for differences in version parts
            if remote_major != local_major:
                update_level = f"{colours.BOLD_RED}{self.version_cls.major[1]}{colours.BOLD_RED_RESET}"

            elif remote_minor != local_minor:
                update_level = f"{colours.BOLD_YELLOW}{self.version_cls.minor[1]}{colours.BOLD_YELLOW_RESET}"

            elif remote_patch != local_patch:
                update_level = f"{colours.BOLD_GREEN}{self.version_cls.patch[1]}{colours.BOLD_GREEN_RESET}"

            if update_level:
                logger.info(
                    f"🔄 {update_level} update is available [{colours.CYAN}{remote_version_str}{colours.CYAN_RESET}]"
                )

    @staticmethod
    def is_docker_container() -> bool:
        """
        Determines if the program is running inside a Docker container.

        :return: True if running inside a Docker container, otherwise False.
        :rtype: bool
        """
        return os.environ.get("IS_DOCKER_CONTAINER") == "1"

    @staticmethod
    def is_snap_package() -> bool:
        """
        Checks if a specified package name is installed as a snap package
        by checking if it's running inside a SNAP environment.

        :return: True if the specified package is installed as a snap package, otherwise False.
        :rtype: bool
        """

        return True if os.getenv("SNAP") else False

    def is_pypi_package(self) -> bool:
        """
        Checks if a specified package name is installed as a pypi package.

        :return: True if the specified package is installed as a pypi package, otherwise False.
        :rtype: bool
        """

        try:
            __import__(name=self.package_name)
            return True
        except ImportError:
            return False


# -------------------------------- END ----------------------------------------- #
