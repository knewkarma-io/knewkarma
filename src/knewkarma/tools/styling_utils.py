__all__ = ["Text", "Prefix"]


class Text:
    """
    A class containing rich formatting codes for styling text.

    Attributes:
        blue (str): Rich code for blue text.
        green (str): Rich code for green text.
        yellow (str): Rich code for yellow text.
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
    red: str = "[red]"
    white: str = "[white]"
    reset: str = "[/]"


class Prefix:
    """
    A class for generating styled message prefixes with icons.

    Attributes:
        error (str): A styled prefix for error messages, displaying a red '✘'.
        warning (str): A styled prefix for warning messages, displaying a yellow '✘'.
        ok (str): A styled prefix for successful operations, displaying a green '✔'.
        notify (str): A styled prefix for general notifications, displaying a green '*'.
    """

    error: str = f"[{Text.red}✘{Text.reset}]"
    warning: str = f"[{Text.yellow}✘{Text.reset}]"
    ok: str = f"[{Text.green}✔{Text.reset}]"
    notify: str = f"[{Text.green}*{Text.reset}]"


# -------------------------------- END ----------------------------------------- #
