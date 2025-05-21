import typing as t
from datetime import datetime, timezone
from types import SimpleNamespace

from rich.console import RenderableType, Group
from rich.markdown import Markdown
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

from engines.klaus import RedditEndpoints
from toolbox import colours
from toolbox.logging import console

__all__ = ["Render"]


class Render:
    @classmethod
    def timestamp_to_relative(cls, unix_timestamp: float) -> str:
        """
        Converts a UNIX timestamp to relative time format.

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
            return f"{seconds // minute}m ago"
        elif seconds < day:
            return f"{seconds // hour}h ago"
        elif seconds < week:
            return f"{seconds // day}d ago"
        elif seconds < month:
            return f"{seconds // week}w ago"
        elif seconds < year:
            return f"{seconds // month}mo ago"
        else:
            return f"{seconds // year}y ago"

    @classmethod
    def posts(cls, data: t.List[SimpleNamespace]):
        """Print panels for displaying posts/comments."""
        panels: t.List[Panel] = []

        for item in data:
            post = item.data
            panel_parts: t.List = []

            is_comment: bool = hasattr(post, "body") and not hasattr(post, "selftext")
            is_post: bool = not is_comment

            title: str = getattr(post, "title", "")
            selftext: str = getattr(post, "selftext", "")
            body: str = getattr(post, "body", "")
            permalink: str = getattr(post, "permalink", "")
            url: str = getattr(post, "url", "")
            subreddit_name: str = getattr(post, "subreddit_name_prefixed", "")
            author: str = getattr(post, "author", "")
            created: int = getattr(post, "created", int)
            comments: int = getattr(post, "num_comments", int)
            replies: t.List = getattr(post, "replies", [])
            is_nsfw: bool = getattr(post, "over_18", False)

            if title:
                panel_parts.append(f"**{title}**")

            panel_parts.append(selftext) if selftext else panel_parts.append(body) if body else None

            text: str = "\n\n".join(panel_parts)

            header_content: str = (
                f"{colours.BOLD}{subreddit_name}{colours.RESET} · {colours.BOLD_BLUE}"
                f"{f'[link={RedditEndpoints.BASE}/{permalink}]View on Reddit[/link]'
                           if is_comment else 
                f'[link={url}]View on Reddit[/link]'}{colours.BOLD_BLUE_RESET}\nu/{author}"
                f" · {colours.BOLD_BLACK}{cls.timestamp_to_relative(unix_timestamp=created)}"
                f"{colours.BOLD_BLACK_RESET}"
            )

            footer_content: str = (
                f"{colours.ORANGE_RED}🡅{post.ups}{colours.RESET} "
                f" {colours.SOFT_BLUE}🡇{post.downs}{colours.RESET} "
                f" {colours.WHITE}🗩 {comments if is_post else len(replies)}{colours.WHITE_RESET} "
                f" {colours.BOLD_YELLOW}🎖{len(post.all_awardings)}{colours.BOLD_YELLOW_RESET}"
            )

            if is_nsfw:
                header_content: str = (
                    f"{colours.BOLD_RED}NSFW{colours.BOLD_RED_RESET} · {header_content}"
                )

            panel = cls.panel(
                header=header_content,
                content=text,
                footer=footer_content,
                add_dividers=True,
            )

            panels.append(panel)

        panel_group = Group(*panels)

        console.print(panel_group)

    @classmethod
    def subreddit_profile(cls, data: SimpleNamespace):
        cls.panel(
            header=(
                f"{data.display_name_prefixed} · "
                f"[bold black]{cls.timestamp_to_relative(unix_timestamp=data.created)}[/bold black]"
                f" · {data.public_description}"
            ),
            content=data.description,
            footer=f"Subscribers {data.subscribers}  Active Accounts {data.accounts_active}",
            print_panel=True,
        )

    @classmethod
    def panel(
        cls,
        content: t.Union[str, RenderableType],
        header: t.Optional[str] = None,
        footer: t.Optional[str] = None,
        **kwargs,
    ) -> Panel:
        """
        Builds and optionally prints a styled Rich Panel.

        Supports Markdown-formatted string content or any Rich renderable (e.g., Tree, Table, Markdown).
        Header and footer are rendered using Rich markup. Various display options can be controlled via kwargs.

        :param content: The main body of the panel. If a string is passed, it is rendered as Markdown.
        :type content: Union[str, RenderableType]
        :param header: Optional panel header, rendered using Rich markup.
        :type header: Optional[str]
        :param footer: Optional panel footer, rendered using Rich markup.
        :type footer: Optional[str]
        :keyword print_panel: Whether to immediately print the panel to the console.
        :keyword show_outline: Whether to show a visible white border around the panel.
        :keyword add_dividers: Whether to add horizontal dividers between header, content, and footer.
        :keyword divider_visibility: Whether dividers should be visible or hidden (color-wise).
        Accepted values: "visible", "hidden". Defaults to "hidden".
        :return: A styled Rich Panel containing the given content.
        :rtype: Panel
        """

        print_panel: bool = kwargs.get("print_panel", False)
        show_outline: bool = kwargs.get("show_outline", True)
        add_dividers: bool = kwargs.get("add_dividers", True)

        div_visibility_literals = t.Literal["visible", "hidden"]
        divider_visibility: t.Literal["visible", "hidden"] = t.cast(
            div_visibility_literals, kwargs.get("divider_visibility", "hidden")
        )

        divider_style: str = "#444444" if divider_visibility == "visible" else "black"
        content_items: t.List[RenderableType] = []

        if header:
            header_renderable = Text.from_markup(
                header, justify="left", overflow="ellipsis"
            )
            content_items.append(header_renderable)
            if add_dividers:
                content_items.append(Rule(style=divider_style))

        if isinstance(content, str):
            content_renderable = Markdown(content, justify="left", style="white")
        else:
            content_renderable = content

        content_items.append(content_renderable)

        if footer:
            if add_dividers:
                content_items.append(Rule(style=divider_style))
            footer_renderable = Text.from_markup(
                footer, justify="left", overflow="ellipsis"
            )
            content_items.append(footer_renderable)

        # content_items.append(Rule(style="#444444"))

        group = Group(*content_items)

        panel = Panel(
            renderable=group,
            border_style="#444444" if show_outline else "black",
            title_align="left",
        )

        if print_panel:
            console.print(panel)

        return panel

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
