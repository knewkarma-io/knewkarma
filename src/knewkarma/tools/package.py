import os
import subprocess

from rich.console import Console

from .console import Notify

__all__ = ["is_pypi_package", "is_snap_package", "update_pypi_package"]

notify = Notify


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
        notify.raise_exception(
            ValueError, "The provided package name is not a valid string."
        )


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
        notify.raise_exception(
            ValueError, "The provided package name is not a valid string."
        )


def update_pypi_package(package: str, status: Console.status = None):
    """
    Updates a specified pypi package.

    :param package: Name of the pypi package to update.
    :type package: str
    :param status: An optional `console.status` object for displaying status messages.
    :type status: rich.console.Console.status, optional

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
                notify.update_status(status=status, message="Downloading updates")
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
            notify.ok(f"DONE. The updates will be applied on next run.")
        except subprocess.CalledProcessError as called_process_error:
            notify.exception(
                error=called_process_error,
                exception_context=f"while updating {package}",
            )
        except Exception as unexpected_error:
            notify.exception(
                error=unexpected_error,
                exception_type="unexpected",
                exception_context=f"while updating {package}",
            )
    else:
        notify.raise_exception(
            ValueError, "The provided package name is not a valid string."
        )


# -------------------------------- END ----------------------------------------- #
