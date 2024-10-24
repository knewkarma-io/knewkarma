import os
import subprocess
from typing import Optional, List

import aiohttp
from rich.markdown import Markdown
from rich.status import Status

from .general import General
from .terminal import Message, Style

__all__ = ["Package"]


class Package:
    def __init__(self, name: str, **kwargs):

        self._package = name
        self._version = kwargs.get("version")
        self._send_request = kwargs.get("requester")
        self._invalid_package_error = (
            f"The provided package name is not a valid string: {name}"
        )

    async def check_updates(
        self,
        session: aiohttp.ClientSession,
        status: Optional[Status] = None,
        install_if_available: bool = False,
    ):
        """
        Asynchronously checks for updates by comparing the current local version with the remote version.

        Assumes version format: major.minor.patch.prefix

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param status: An optional `Status` object for displaying status messages.
        :type status: Optional[rich.status.Status]
        """

        if status:
            status.update("Checking for updates")

        # Make a GET request to GitHub to get the project's latest release.
        response = await self._send_request(
            endpoint=f"https://api.github.com/repos/knewkarma-io/{self._package}/releases/latest",
            session=session,
        )

        if response.get("tag_name"):
            remote_version_str = response.get("tag_name")
            markup_release_notes = response.get("body")

            # Splitting the version strings into components
            local_version_parts = [
                self._version.major[0],
                self._version.minor[0],
                self._version.patch[0],
            ]
            remote_version_parts: List = remote_version_str.split(".")

            local_major: int = local_version_parts[0]
            local_minor: int = local_version_parts[1]
            local_patch: int = local_version_parts[2]

            remote_major = int(remote_version_parts[0])
            remote_minor = int(remote_version_parts[1])
            remote_patch = int(remote_version_parts[2])

            update_level = ""

            # Check for differences in version parts
            if remote_major != local_major:
                update_level = f"{Style.red}{self._version.major[1]}{Style.reset}"

            elif remote_minor != local_minor:
                update_level = f"{Style.yellow}{self._version.minor[1]}{Style.reset}"

            elif remote_patch != local_patch:
                update_level = f"{Style.green}{self._version.patch[1]}{Style.reset}"

            if update_level:
                markdown_release_notes = Markdown(markup=markup_release_notes)
                General.make_panel(
                    title=f"{Style.bold}{update_level} Update Available ({Style.cyan}{remote_version_str}{Style.reset}){Style.reset}",
                    content=markdown_release_notes,
                    subtitle=f"{Style.bold}{Style.italic}Thank you, for using Knew Karma!{Style.reset}{Style.reset} ❤️ ",
                )

                if install_if_available:
                    self.update_package(status=status)
            else:
                Message.ok(message=f"No new releases")

    @staticmethod
    def is_docker_container() -> bool:
        """
        Determines if the program is running inside a Docker container.

        :return: True if running inside a Docker container, otherwise False.
        :rtype: bool
        """
        return os.environ.get("IS_DOCKER_CONTAINER") == "1"

    def is_snap_package(self) -> bool:
        """
        Checks if a specified package name is installed as a snap package
        by checking if it's running inside a SNAP environment.

        :return: True if the specified package is installed as a snap package, otherwise False.
        :rtype: bool
        """

        if self._package:
            return True if os.getenv("SNAP") else False
        else:
            Message.error(self._invalid_package_error)

    def is_pypi_package(self) -> bool:
        """
        Checks if a specified package name is installed as a pypi package.

        :return: True if the specified package is installed as a pypi package, otherwise False.
        :rtype: bool
        """

        if self._package:
            try:
                __import__(name=self._package)
                return True
            except ImportError:
                return False
        else:
            Message.error(self._invalid_package_error)

    def update_package(self, status: Optional[Status] = None):
        """
        Updates a specified pypi package.

        :param status: An optional `Status` object for displaying status messages.
        :type status: rich.status.Status
        """

        if self.is_snap_package():
            Message.warning("Run 'snap refresh knewkarma' to update the snap package.")
        else:
            if self._package:
                try:
                    if status:
                        status.stop()
                        # status.update("Downloading updates. Please wait")
                    subprocess.run(
                        [
                            "pip",
                            "install",
                            "--upgrade",
                            f"{self._package}[core]",
                        ],
                        check=True,
                    )
                    Message.ok(f"DONE. The updates will be installed on next run.")
                except subprocess.CalledProcessError as called_process_error:
                    Message.exception(
                        title=f"An error occurred ({Style.italic}while updating package{Style.reset})",
                        error=called_process_error,
                    )
                except Exception as unexpected_error:
                    Message.exception(unexpected_error)
            else:
                Message.error(self._invalid_package_error)


# -------------------------------- END ----------------------------------------- #
