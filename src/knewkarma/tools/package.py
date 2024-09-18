import os
import subprocess
from typing import Optional, List

import aiohttp
from rich.markdown import Markdown
from rich.prompt import Confirm
from rich.status import Status

from .miscellaneous import make_panel
from ..meta import about, version
from ..shared_imports import api, console, notify, style

__all__ = [
    "check_for_updates",
    "is_pypi_package",
    "is_snap_package",
    "update_package",
]

INVALID_PACKAGE_ERROR: str = (
    "The provided package name is not a valid string: {package}"
)


def is_snap_package(package: str) -> bool:
    """
    Checks if a specified package name is installed as a snap package
    by checking if it's running inside a SNAP environment.

    :param package: Name of the package to check.
    :type package: str
    :return: True if the specified package is installed as a snap package, otherwise False.
    :rtype: bool

    Usage::

        >>> from knewkarma.tools.package import is_snap_package

        >>> package_name = "src"
        >>> print(is_snap_package(package=package_name))
        >>> False # If script isn't running in a SNAP environment.
    """

    if package:
        return True if os.getenv("SNAP") else False
    else:
        notify.error(INVALID_PACKAGE_ERROR.format(package=package))


def is_pypi_package(package: str) -> bool:
    """
    Checks if a specified package name is installed as a pypi package.

    :param package: Name of the package to check.
    :type package: str
    :return: True if the specified package is installed as a pypi package, otherwise False.
    :rtype: bool

    Usage::

        >>> from knewkarma.tools.package import is_pypi_package

        >>> package_name = "src"
        >>> print(is_pypi_package(package=package_name))
        >>> True
    """

    if package:
        try:
            __import__(name=package)
            return True
        except ImportError:
            return False
    else:
        notify.error(INVALID_PACKAGE_ERROR.format(package=package))


async def check_for_updates(
        session: aiohttp.ClientSession, status: Optional[Status] = None
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
    response = await api.make_request(
        endpoint=f"https://api.github.com/repos/{about.author[1]}/{about.package}/releases/latest",
        session=session,
    )

    if response.get("tag_name"):
        remote_version_str = response.get("tag_name")
        markup_release_notes = response.get("body")

        # Splitting the version strings into components
        local_version_parts = [
            version.major[0],
            version.minor[0],
            version.patch[0],
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
            update_level = f"{style.red}{version.major[1]}{style.reset}"

        elif remote_minor != local_minor:
            update_level = f"{style.yellow}{version.minor[1]}{style.reset}"

        elif remote_patch != local_patch:
            update_level = f"{style.green}{version.patch[1]}{style.reset}"

        if update_level:
            markdown_release_notes = Markdown(markup=markup_release_notes)
            make_panel(
                title=f"{style.bold}{update_level} Update Available ({style.cyan}{remote_version_str}{style.reset}){style.reset}",
                content=markdown_release_notes,
                subtitle=f"{style.bold}{style.italic}Thank you, for using {about.name}!{style.reset}{style.reset} ❤️ ",
            )

            # Skip auto-updating of the snap package
            if not is_snap_package(package=about.package):
                status.stop()
                if Confirm.ask(
                        f"{style.bold}Would you like to get these updates?{style.reset}",
                        case_sensitive=False,
                        default=False,
                        console=console,
                ):
                    update_package(package=about.package, status=status)
                else:
                    status.start()
        else:
            notify.ok(message=f"Up-to-date ({version.full})")


def update_package(package: str, status: Optional[Status] = None):
    """
    Updates a specified pypi package.

    :param package: Name of the pypi package to update.
    :type package: str
    :param status: An optional `Status` object for displaying status messages.
    :type status: rich.status.Status

    Usage::

        >>> from knewkarma.tools.package import update_pypi_package

        >>> # This will update the pypi package
        >>> package_name = "src"
        >>> update_pypi_package(package=package_name)
    """

    if package:
        try:
            if status:
                status.start()
                status.update("Downloading updates")
            subprocess.run(
                [
                    "pip",
                    "install",
                    "--upgrade",
                    package,
                ],
                check=True,
                stdout=subprocess.DEVNULL if status else None,
                stderr=subprocess.STDOUT if status else None,
            )
            notify.ok(f"DONE. The updates will be installed on next run.")
        except subprocess.CalledProcessError as called_process_error:
            notify.exception(
                title=f"An error occurred ({style.italic}while updating package{style.reset})",
                error=called_process_error,
            )
        except Exception as unexpected_error:
            notify.exception(unexpected_error)
    else:
        notify.error(INVALID_PACKAGE_ERROR.format(package=package))

# -------------------------------- END ----------------------------------------- #
