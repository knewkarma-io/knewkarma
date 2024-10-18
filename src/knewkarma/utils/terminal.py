from rich.console import Console

__all__ = ["console", "Message", "Style"]

console = Console(log_time=False)


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


class Message:
    """
    Provides static methods for printing and/or logging formatted notifications to the console.
    """

    @staticmethod
    def ok(message: str):
        """
        Prints a `success` message (with a checkmark).

        :param message: Text to be logged.
        :type message: str
        """

        console.print(f"{Style.green}✔{Style.reset} {message}")

    @staticmethod
    def info(message: str):
        """
        Prints an `informational` message to the console.

        :param message: Text to be logged.
        :type message: str
        """

        console.print(f"{Style.green}✱{Style.reset} {message}")

    @staticmethod
    def warning(message: str):
        """
        Prints a `warning` message to the console.

        :param message: Text to be logged.
        :type text: str
        """

        console.print(f"{Style.yellow}✘{Style.reset} {message}")

    @staticmethod
    def error(text: str):
        """
        Logs an error with the specified message to the console.

        :param text: Error message to be logged.
        :type text: str
        """

        console.log(f"{Style.yellow}✘{Style.reset} {message}")

    @staticmethod
    def exception(error: Exception, title: str = "An unexpected error occurred"):
        """
        Logs an exception message to the console.

        :param title: Title of the error (e.g., "An exception occurred")
        :type title: str
        :param error: Error that triggered the exception.
        :type error: Exception
        """

        console.log(f"{Style.red}✘{Style.reset} {title}: {error}")


# -------------------------------- END ----------------------------------------- #
