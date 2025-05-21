import typing as t
from datetime import datetime, timezone
from types import SimpleNamespace

from rich.console import RenderableType, Group
from rich.markdown import Markdown
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

from toolbox import colours
from toolbox.logging import console

__all__ = ["Render"]


class Render:
    @classmethod
    def _time_ago_from_unix(cls, unix_timestamp: float) -> str:
        """
        Converts a UNIX timestamp to Reddit-style relative time format.

        Examples:
            - Just now
            - 2m ago
            - 3h ago
            - 5d ago
            - 2w ago
            - 4mo ago
            - 1y ago
        """
        now = datetime.now(timezone.utc)
        then = datetime.fromtimestamp(unix_timestamp, tz=timezone.utc)
        delta = now - then
        seconds = int(delta.total_seconds())

        if seconds < 0:
            return "Just now"  # Reddit doesn’t display "in X minutes"

        minute = 60
        hour = 60 * minute
        day = 24 * hour
        week = 7 * day
        month = 30 * day  # approx
        year = 365 * day  # approx

        if seconds < minute:
            return "Just now"
        elif seconds < hour:
            return f"{seconds // minute} min. ago"
        elif seconds < day:
            return f"{seconds // hour} hr. ago"
        elif seconds < week:
            return f"{seconds // day} day. ago"
        elif seconds < month:
            return f"{seconds // week} wk. ago"
        elif seconds < year:
            return f"{seconds // month} mo. ago"
        else:
            return f"{seconds // year} yr. ago"

    @classmethod
    def panel(
        cls,
        header_text: str,
        content_text: str,
        footer_text: str = "Hello",
        print_panel: bool = False,
        show_outline: bool = True,
        add_dividers: bool = True,
        divider_visibility: t.Literal["visible", "hidden"] = "hidden",
    ) -> Panel:
        """
        Wraps the given header, content, and metadata into a styled Rich Panel.
        """

        divider_style: str = "#444444" if divider_visibility == "visible" else "black"
        header = Text.from_markup(text=header_text, justify="left", overflow="ellipsis")
        content = Markdown(markup=content_text, justify="left", style="white")

        meta_info = Text()
        if footer_text:
            meta_info = Text.from_markup(
                text=footer_text, justify="left", overflow="ellipsis"
            )

        content_items: t.List[RenderableType] = [header]

        if add_dividers:
            content_items.append(Rule(style=divider_style))

        content_items.append(content)

        if add_dividers:
            content_items.append(Rule(style=divider_style))

        content_items.append(meta_info)
        content_items.append(Rule(style="#444444"))
        group = Group(*content_items)

        panel = Panel(
            renderable=group,
            border_style=None if show_outline else "black",
            title_align="left",
        )

        if print_panel:
            console.print(panel)

        return panel

    @classmethod
    def panels(
        cls, data: t.Union[t.List[SimpleNamespace], SimpleNamespace, str], **kwargs
    ):
        """
        Print panels for displaying code or structured file information.

        Accepts either:
          - a single SimpleNamespace with fields `code`, `language`
          - a string of raw code
          - a list of SimpleNamespace objects with fields `filename`, `repo`, `language`, `linescount`, `lines`

        :param data: The input data to display as panels.
        :type data: Union[List[SimpleNamespace], SimpleNamespace, str]
        :param kwargs: Additional optional keyword arguments (e.g., id for logging).
        :type kwargs: Any
        """
        inner_panels: t.List[Panel] = []

        for item in data:
            parts = []

            title = getattr(item.data, "title", "")
            selftext = getattr(item.data, "selftext", "")

            if title:
                parts.append(f"**[{title}]({item.data.url})**")
            if selftext:
                parts.append(selftext)

            text = "\n\n".join(parts)

            header_text = f"u/{item.data.author} · [bold black]{cls._time_ago_from_unix(unix_timestamp=item.data.created)}[/bold black]"

            if item.data.over_18:
                header_text = (
                    f"{colours.BOLD_RED}NSFW{colours.BOLD_RED_RESET} · {header_text}"
                )

            inner_panel = cls.panel(
                header_text=header_text,
                content_text=text,
                footer_text=f"{colours.ORANGE_RED}🡅{item.data.ups}{colours.RESET} "
                f" {colours.SOFT_BLUE}🡇{item.data.downs}{colours.RESET} "
                f" {colours.WHITE}🗩 {item.data.num_comments}{colours.WHITE_RESET} "
                f" {colours.BOLD_YELLOW}🎖{len(item.data.all_awardings)}{colours.BOLD_YELLOW_RESET}",
                add_dividers=True,
                show_outline=False,
            )

            inner_panels.append(inner_panel)

        group = Group(*inner_panels)

        outer_panel = Panel(renderable=group, title=kwargs.get("title"))

        console.print(outer_panel)

    @classmethod
    def bar_chart(
        cls,
        data: t.Dict[str, int],
        title: str,
        x_label: str,
        y_label: str,
    ):
        """
        Renders a simple bar chart in the terminal using Rich.

        :param data: A dictionary of category-value pairs.
        :param title: Title of the chart.
        :param x_label: Label for the x-axis (shown in the subtitle).
        :param y_label: Label for the y-axis (shown in the subtitle).
        """

        max_value = max(data.values()) or 1  # Avoid divide-by-zero
        table = Table(show_header=False, box=None, expand=True)
        table.add_column("Category", justify="right")
        table.add_column("Bar", justify="left")

        for label, value in data.items():
            bar_length = int((value / max_value) * 40)
            bar = "█" * bar_length
            table.add_row(f"[bold]{label}[/bold]", f"{bar} {value}")

        subtitle = f"{x_label} vs {y_label}" if x_label and y_label else ""
        panel = Panel(
            table, title=f"[bold magenta]{title}[/bold magenta]", subtitle=subtitle
        )
        console.print(panel)
