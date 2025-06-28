import typing as t
from datetime import datetime, timezone

import dateutil.parser
import humanize

from ..riches import rich_colours


class HumanThings:

    @classmethod
    def human_datetime(
        cls, inhuman_datetime: t.Union[float, str], show_clock: bool = True
    ) -> str:
        """
        Converts a UNIX timestamp or ISO 8601 datetime string to a human-readable relative time.
        If parsing fails, returns the original input unchanged.
        """
        if isinstance(inhuman_datetime, float):
            then = datetime.fromtimestamp(inhuman_datetime, tz=timezone.utc)
        else:
            then = dateutil.parser.isoparse(inhuman_datetime)
            if then.tzinfo is None:
                then = then.replace(tzinfo=timezone.utc)
            else:
                then = then.astimezone(timezone.utc)

        now = datetime.now(timezone.utc)
        humanised = humanize.naturaltime(now - then)

        humanised_datetime_string = f"{rich_colours.GREY}{'⏲ ' if show_clock else ''}{humanised}{rich_colours.RESET}"
        return humanised_datetime_string

    @classmethod
    def human_number(cls, inhuman_number: t.Union[int, float]) -> str:
        """
        Format a number using abbreviations like k, M, B, etc.
        """
        word = humanize.intword(inhuman_number)
        return (
            word.replace(" thousand", "K")
            .replace(" million", "M")
            .replace(" billion", "B")
            .replace(" trillion", "T")
        )
