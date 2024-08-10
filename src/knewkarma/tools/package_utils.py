import os
import subprocess

from .misc_utils import console
from .styling_utils import Prefix

__all__ = ["is_pypi_package", "is_snap_package", "update_pypi_package"]


def is_snap_package(package: str) -> bool:
    """
    Checks if a specified package name is installed as a snap package
    by checking if it's running inside a SNAP environment.

    :param package: Name of the package to check.
    :type package: str
    :return: True if the specified package is installed as a snap package, otherwise False.
    :rtype: bool

    Usage::

        >>> from knewkarma.tools.package_utils import is_snap_package

        >>> package_name = "src"
        >>> print(is_snap_package(package=package_name))
        >>> False # If script isn't running in a SNAP environment.
    """
    if package:
        return True if os.getenv("SNAP") else False
    else:
        raise ValueError("Empty package name provided.")


def is_pypi_package(package: str) -> bool:
    """
    Checks if a specified package name is installed as a pypi package.

    :param package: Name of the package to check.
    :type package: str
    :return: True if the specified package is installed as a pypi package, otherwise False.
    :rtype: bool

    Usage::

        >>> from knewkarma.tools.package_utils import is_pypi_package

        >>> package_name = "src"
        >>> print(is_pypi_package(package=package_name))
        >>> True
    """
    if package:
        try:
            # Try to import the package to see if it exists
            __import__(name=package)
            return True
        except ImportError:
            return False
    else:
        raise ValueError("Empty package name provided.")


def update_pypi_package(package: str):
    """
    Updates a specified pypi package.

    :param package: Name of the pypi package to update.
    :type package: str

    Usage::

        >>> from knewkarma.tools.package_utils import update_pypi_package

        >>> # This will update the pypi package
        >>> package_name = "src"
        >>> update_pypi_package(package=package_name)
    """
    if package:
        try:
            subprocess.run(["pip", "install", "--upgrade", package], check=True)
            console.print(f"{Prefix.ok} DONE. Updates will be applied on next run.")
        except subprocess.CalledProcessError as e:
            console.log(f"{Prefix.error} Failed to update {package}: {e}")
        except Exception as e:
            console.log(f"{Prefix.error} Unexpected error: {e}")
    else:
        raise ValueError("Empty package name provided.")


# -------------------------------- END ----------------------------------------- #
