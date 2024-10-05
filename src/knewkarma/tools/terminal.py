from rich.console import Console

__all__ = ["Notify", "Style"]


class Style:
    """
    Provides rich formatting codes for styling console text.

    Attributes:
        blue (str): Rich code for blue text.
        bold (str): Rich code for bold text.
        cyan (str): Rich code for cyan text.
        green (str): Rich code for green text.
        italic (str): Rich code for italic text.
        yellow (str): Rich code for yellow text.
        purple (str): Rich code for purple text.
        red (str): Rich code for red text.
        white (str): Rich code for white text.
        reset (str): Rich code to reset text formatting.
    """

    blue: str = "[blue]"
    bold: str = "[bold]"
    cyan: str = "[cyan]"
    green: str = "[green]"
    italic: str = "[italic]"
    yellow: str = "[yellow]"
    purple: str = "[purple]"
    red: str = "[red]"
    white: str = "[white]"
    reset: str = "[/]"


class Notify:
    """
    Provides methods for printing and/or logging formatted notifications to the console.
    """

    def __init__(self, console: Console):
        self._console = console

    def ok(self, message: str):
        """
        Prints a `success` message (with a checkmark).

        :param message: Message to be logged.
        :type message: str
        """

        self._console.print(f"{Style.green}✔{Style.reset} {message}")

    def info(self, message: str):
        """
        Prints an `informational` message to the console.

        :param message: Message to be logged.
        :type message: str
        """

        self._console.print(f"{Style.green}✱{Style.reset} {message}")

    def warning(self, message: str):
        """
        Prints a `warning` message to the console.

        :param message: Message to be logged.
        :type message: str
        """

        self._console.print(f"{Style.yellow}✘{Style.reset} {message}")

    def error(self, message: str):
        """
        Logs an error with the specified message to the console.

        :param message: Error message to be logged.
        :type message: str
        """

        self._console.log(f"{Style.yellow}✘{Style.reset} {message}")

    def exception(self, error: Exception, title: str = "An unexpected error occurred"):
        """
        Logs an exception message to the console.

        :param title: Title of the error (e.g., "An exception occurred")
        :type title: str
        :param error: Error that triggered the exception.
        :type error: Exception
        """

        self._console.log(f"{Style.red}✘{Style.reset} {title}: {error}")


# -------------------------------- END ----------------------------------------- #
