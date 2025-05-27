import os
import typing as t

import aiohttp
from rich.status import Status

from knewkarma.core.models import reddit
from knewkarma.metadata.about import Project
from knewkarma.metadata.version import Version
from . import colours
from .logging import logger

__all__ = ["Runtime"]


class Runtime:
    _PACKAGE = Project.package
    _VERSION = Version
    _REQ_HANDLER = reddit.request_handler.send_request

    @classmethod
    async def check_updates(
        cls,
        session: aiohttp.ClientSession,
        status: t.Optional[Status] = None,
    ):
        """
        Asynchronously checks for updates by comparing the current local version with the remote version.

        Assumes version format: major.minor.patch.prefix

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param status: An optional `Status` object for displaying status messages.
        :type status: t.Optional[rich.status.Status]
        """

        if status:
            status.update("Checking for updates")

        # Make a GET request to GitHub to get the project's latest release.
        response = await cls._REQ_HANDLER(
            endpoint=f"https://api.github.com/repos/knewkarma-io/{cls._PACKAGE}/releases/latest",
            session=session,
        )

        if response.get("tag_name"):
            remote_version_str = response.get("tag_name")

            # Splitting the version strings into components
            local_version_parts = [
                cls._VERSION.major[0],
                cls._VERSION.minor[0],
                cls._VERSION.patch[0],
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
                update_level = (
                    f"{colours.BOLD_RED}{cls._VERSION.major[1]}{colours.BOLD_RED_RESET}"
                )

            elif remote_minor != local_minor:
                update_level = f"{colours.BOLD_YELLOW}{cls._VERSION.minor[1]}{colours.BOLD_YELLOW_RESET}"

            elif remote_patch != local_patch:
                update_level = f"{colours.BOLD_GREEN}{cls._VERSION.patch[1]}{colours.BOLD_GREEN_RESET}"

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

    @classmethod
    def is_snap_package(cls) -> bool:
        """
        Checks if a specified package name is installed as a snap package
        by checking if it's running inside a SNAP environment.

        :return: True if the specified package is installed as a snap package, otherwise False.
        :rtype: bool
        """

        return True if os.getenv("SNAP") else False

    @classmethod
    def is_pypi_package(cls) -> bool:
        """
        Checks if a specified package name is installed as a pypi package.

        :return: True if the specified package is installed as a pypi package, otherwise False.
        :rtype: bool
        """

        try:
            __import__(name=cls._PACKAGE)
            return True
        except ImportError:
            return False


# -------------------------------- END ----------------------------------------- #
