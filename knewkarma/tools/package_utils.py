import subprocess
from typing import Literal

__all__ = ["is_pypi_package", "is_snap_package", "update_package"]

from .general_utils import console


def is_snap_package(package: str) -> bool:
    """
    Checks if a specified package name is installed as a snap package.

    :param package: Name of the package to check.
    :type package: str
    :return: True if the specified package is installed as a snap package, otherwise False.
    :rtype: bool

    Usage::

        >>> from knewkarma.tools.package_utils import is_pypi_package

        >>> package_name = "knewkarma"
        >>> print(is_pypi_package(package=package_name))
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
        except Exception as e:
            console.log(f"[red]✘[/] Error checking snap packages: {e}")
        return False
    else:
        raise ValueError(f"Empty package name provided.")


def is_pypi_package(package: str) -> bool:
    """
    Checks if a specified package name is installed as a pypi package.

    :param package: Name of the package to check.
    :type package: str
    :return: True is the specified package is installed as a pypi package, otherwise False.
    :rtype: bool

    Usage::

        >>> from knewkarma.tools.package_utils is_snap_package

        >>> # Assuming snap is installed
        >>> package_name = "knewkarma-something-something-something"
        >>> print(is_snap_package(package=package_name))
        >>> False
    """
    if package:
        try:
            # Try to import the package to see if it exists
            __import__(name=package)
            return True
        except ImportError:
            return False
    else:
        raise ValueError(f"Empty package name provided.")


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
            if package_type == "pypi":
                subprocess.run(["pip", "install", "--upgrade", package])
            elif package == "snap":
                subprocess.run(["sudo", "snap", "refresh", package])

            console.print(
                f"[green]✔[/] DONE. Updates will be applied on next run."
            )
        except Exception as e:
            console.log(f"[red]✘[/] Failed to update {package}: {e}")
    else:
        raise ValueError(f"Empty package name provided.")

# -------------------------------- END ----------------------------------------- #
