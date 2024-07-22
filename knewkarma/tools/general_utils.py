import os

from rich.console import Console
from rich.table import Table


def print_banner():
    """
    Prints the projects banner and system information.

    Usage::

        >>> from knewkarma.tools.general_utils import print_banner

        >>> print_banner()
    """
    console.log(
        f"""
┓┏┓         ┓┏┓
┃┫ ┏┓┏┓┓┏┏  ┃┫ ┏┓┏┓┏┳┓┏┓
┛┗┛┛┗┗ ┗┻┛  ┛┗┛┗┻┛ ┛┗┗┗┻"""
    )
    console.print(get_system_info())


def get_system_info() -> Table:
    """
    Gets system information

    :return: A table containing system information.
    :rtype: rich.table.Table

    Usage::

        >>> from knewkarma.tools.general_utils import get_system_info
        >>> from rich import print as xprint

        >>> xprint(get_system_info())
    """
    import getpass
    import platform
    import sys

    import psutil

    from .time_utils import _time_since
    from ..version import Version

    table = Table(show_header=False, show_edge=False, highlight=True)
    table.add_column("header", style="dim")
    table.add_column("header")

    # https://www.geeksforgeeks.org/getting-the-time-since-os-startup-using-python/
    if os.name == "nt":
        # ctypes required for using GetTickCount64()
        import ctypes

        # getting the library in which GetTickCount64() resides
        lib = ctypes.windll.kernel32

        # calling the function and storing the return value
        t = lib.GetTickCount64()

        # since the time is in milliseconds i.e. 1000 * seconds
        # therefore truncating the value
        t = int(str(t)[:-3])

        # extracting hours, minutes, seconds & days from t
        # variable (which stores total time in seconds)
        minutes, seconds = divmod(t, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        system_uptime = (
            "just now"
            if days == hours == minutes == seconds == 0
            else f"{days} days, {hours:02} hours, {minutes:02} minutes, and {seconds:02} seconds since boot"
        )
    else:
        system_uptime = _time_since(
            timestamp=int(psutil.boot_time()), suffix="since boot"
        )

    table.add_row("Username", getpass.getuser())
    table.add_row("Knew Karma", Version.full)
    table.add_row("Python", sys.version)
    table.add_row("System", f"{platform.system()} {platform.version()}")
    table.add_row(
        "CPU", f"{psutil.cpu_count(logical=True)} cores, {platform.processor()}"
    )
    table.add_row(
        "Disk",
        f"{psutil.disk_usage('/').free / (1024**3):.2f} GB free"
        f" / {psutil.disk_usage('/').total / (1024**3):.2f} GB",
    )
    table.add_row(
        "Memory",
        f"{psutil.virtual_memory().available / (1024**3):.2f} GB free"
        f" / {psutil.virtual_memory().total / (1024**3):.2f} GB",
    )

    table.add_row(
        "Uptime",
        system_uptime,
    )

    return table


def pathfinder(directories: list[str]):
    """
    Creates directories in knewkarma-output directory of the user's home folder.

    :param directories: A list of file directories to create.
    :type directories: list[str]
    """
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


console = Console(color_system="auto", log_time=False)
