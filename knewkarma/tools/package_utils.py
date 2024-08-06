import subprocess
from typing import Literal

from .general_utils import console

__all__ = ["is_pypi_package", "is_snap_package", "update_package"]


def is_snap_package(package: str) -> bool:
    """
    Checks if a specified package name is installed as a snap package.

    :param package: Name of the package to check.
    :type package: str
    :return: True if the specified package is installed as a snap package, otherwise False.
    :rtype: bool

    Usage::

        >>> from knewkarma.tools.package_utils import is_snap_package

        >>> package_name = "knewkarma"
        >>> print(is_snap_package(package=package_name))
        >>> True
    """
    if package:
        try:
            # List installed snaps and check if the package is among them
            result = subprocess.run(
                ["snap", "list"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            if result.returncode == 0:
                installed_snaps = result.stdout
                if package in installed_snaps:
                    return True
        except subprocess.CalledProcessError as e:
            console.log(f"[red]✘[/] Error checking snap packages: {e}")
        return False
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

        >>> package_name = "knewkarma"
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


def update_package(package: str, package_type: Literal["pypi", "snap"]):
    """
    Updates a specified package based on what type of package it is.

    :param package: Name of package to update.
    :type package: str
    :param package_type: The type of package being updated. Choose between "pypi" or "snap".
    :type package_type: Literal[str]

    Usage::

        >>> from knewkarma.tools.package_utils import update_package

        >>> # This will update the pypi package
        >>> package_name = "knewkarma"
        >>> update_package(package=package_name, package_type="pypi")

        >>> # Alternatively, this will attempt to update the snap package,
        >>> # (assuming the knewkarma snap package is installed)
        >>> update_package(package=package_name, package_type="snap")
    """
    if package:
        try:
            if package_type == "pypi" and is_pypi_package(package=package):
                subprocess.run(["pip", "install", "--upgrade", package], check=True)
            elif package_type == "snap" and is_snap_package(package=package):
                subprocess.run(["sudo", "snap", "refresh", package], check=True)
            else:
                raise ValueError(f"Invalid package_type or package not installed: {package_type}")

            console.print(
                f"[green]✔[/] DONE. Updates will be applied on next run."
            )
        except subprocess.CalledProcessError as e:
            console.log(f"[red]✘[/] Failed to update {package}: {e}")
        except Exception as e:
            console.log(f"[red]✘[/] Unexpected error: {e}")
    else:
        raise ValueError("Empty package name provided.")

# -------------------------------- END ----------------------------------------- #
