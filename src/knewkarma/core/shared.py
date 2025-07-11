import typing as t

from karmakrate.riches import rich_colours
from karmakrate.riches.rich_logging import console


def is_empty_data(data: t.List, message: str) -> t.List:
    """
    Check if given data is empty.

    :param data: List of data to check.
    :type data: t.List
    :param message: Message to print if data is empty.
    :type message: str
    :return: An empty list if data is empty, otherwise the original data.
    :rtype: t.List
    """

    if not data:
        console.print(
            f"{rich_colours.BOLD_YELLOW}✘{rich_colours.BOLD_YELLOW_RESET} {message}"
        )
        return []
    else:
        return data
