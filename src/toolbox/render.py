import typing as t
from datetime import datetime, timezone
from types import SimpleNamespace

from engines.klaus import RedditEndpoints
from rich.console import RenderableType, Group
from rich.markdown import Markdown
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text
from toolbox import colours
from toolbox.checkers import Checkers
from toolbox.logging import console

__all__ = ["Render"]


class Render:
    checkers = Checkers

    @classmethod
    def has_attrs(cls, obj: t.Any, attrs: t.List[str]) -> bool:
        """
        Return True if all given attributes exist and are not None on the object.
        """
        return all(
            hasattr(obj, attr) and getattr(obj, attr) is not None for attr in attrs
        )

    @classmethod
    def footer_table(cls, footer_data: t.Dict) -> Table:
        table = Table.grid(padding=(0, 4))
        table.add_row(
            *[
                Text.from_markup(
                    f"{colours.BOLD}{value}{colours.RESET}\n[dim]{label}[/]"
                )
                for label, value in footer_data.items()
            ]
        )

        return table

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
    def show(cls, data: t.Any):
        """
        Dynamically dispatch the appropriate rendering method based on data type.
        """
        if isinstance(data, list) and data:
            item = data[0]
            # Guess based on item shape
            if hasattr(item.data, "selftext") and hasattr(item.data, "title"):
                return cls.posts(data)
            elif hasattr(item.data, "body"):
                return cls.comments(data)
            elif hasattr(item.data, "link_karma"):
                return cls.users(data)
            elif hasattr(item, "data") and hasattr(item.data, "subreddit_type"):
                return cls.subreddits(data)
        elif isinstance(data, SimpleNamespace):
            if hasattr(data.data, "selftext") and hasattr(data.data, "title"):
                return cls.post(data)
            elif hasattr(data.data, "body"):
                return cls.comment(data)
            elif hasattr(data.data, "link_karma"):
                return cls.user(data)
            elif hasattr(data, "data") and hasattr(data.data, "subreddit_type"):
                return cls.subreddit(data.data)

        console.print(
            "[bold red]Unable to determine render type for the given data.[/]"
        )
        return None

    @classmethod
    def user(cls, data: SimpleNamespace, print_panel: bool = True):
        user = getattr(data, "data", None)
        subreddit = getattr(user, "subreddit", None)

        if (
            not user
            or not subreddit
            or not cls.has_attrs(
                user, ["name", "created", "link_karma", "comment_karma"]
            )
        ):
            return None

        description = getattr(subreddit, "public_description", "")

        header_content = (
            f"{colours.BOLD}{user.name}{colours.RESET} · "
            f"{colours.BOLD_BLUE}[link={RedditEndpoints.BASE}{subreddit.url}]"
            f"View on Reddit[/link]{colours.BOLD_BLUE_RESET}\n"
            f"{subreddit.display_name_prefixed} · "
            f"{colours.BOLD_BLACK}{cls.timestamp_to_relative(unix_timestamp=user.created)}"
            f"{colours.BOLD_BLACK_RESET}"
        )

        if subreddit.over_18:
            header_content = (
                f"{colours.BOLD_RED}NSFW{colours.BOLD_RED_RESET} · {header_content}"
            )

        footer_data = {
            "Post Karma": user.link_karma,
            "Comment Karma": user.comment_karma,
            "Total Karma": (
                user.link_karma + user.comment_karma
                if not hasattr(user, "total_karma")
                else user.link_karma + user.comment_karma
            ),
        }

        footer_content = cls.footer_table(footer_data=footer_data)

        panel_parts = []
        if description:
            panel_parts.append(description)

        text = "\n\n".join(panel_parts)

        return cls.panel(
            header=header_content,
            content=text,
            footer=footer_content,
            add_dividers=True,
            print_panel=print_panel,
        )

    @classmethod
    def users(cls, data: t.List[SimpleNamespace], print_panel: bool = True):
        panels = []

        for user_data in data:
            panel = cls.user(user_data, print_panel=print_panel)
            if panel is not None:
                panels.append(panel)

        if panels:
            panel_group = Group(*panels)
            console.print(panel_group)
        else:
            console.print("[dim]No valid users to display.[/]")

    @classmethod
    def comment(cls, data: SimpleNamespace, print_panel: bool = True):
        comment = data.data

        if not comment or not cls.has_attrs(
            comment, ["author", "body", "created", "permalink", "ups", "downs"]
        ):
            return None

        panel_parts: t.List[str] = []

        author: str = getattr(comment, "author", "")
        body: str = getattr(comment, "body", "")
        subreddit: str = getattr(comment, "subreddit_name_prefixed", "")
        subreddit = f"self" if subreddit.lower() == f"u/{author.lower()}" else subreddit
        permalink: str = getattr(comment, "permalink", "")
        created: int = getattr(comment, "created", 0)
        upvotes: int = getattr(comment, "ups", 0)
        downvotes: int = getattr(comment, "downs", 0)
        replies: list = getattr(comment, "replies", [])

        awards: list = getattr(comment, "all_awardings", [])
        is_nsfw: bool = getattr(comment, "over_18", False)

        if body:
            panel_parts.append(body)

        text: str = "\n\n".join(panel_parts)
        header_content: str = (
            f"{colours.BOLD}{subreddit}{colours.RESET} · "
            f"{colours.BOLD_BLUE}[link={RedditEndpoints.BASE}/{permalink}]"
            f"View on Reddit[/link]{colours.BOLD_BLUE_RESET}\nu/{author}"
            f" · {colours.BOLD_BLACK}{cls.timestamp_to_relative(unix_timestamp=created)}"
            f"{colours.BOLD_BLACK_RESET}"
        )

        footer_content: str = (
            f"{colours.ORANGE_RED}🡅{upvotes}{colours.RESET} "
            f"{colours.SOFT_BLUE}🡇{downvotes}{colours.RESET} "
            f"{colours.WHITE}🗩 {len(replies)}{colours.WHITE_RESET} "
            f"{colours.BOLD_YELLOW}🎖{len(awards)}{colours.BOLD_YELLOW_RESET}"
        )

        if is_nsfw:
            header_content = (
                f"{colours.BOLD_RED}NSFW{colours.BOLD_RED_RESET} · {header_content}"
            )

        return cls.panel(
            header=header_content,
            content=text,
            footer=footer_content,
            add_dividers=True,
            print_panel=print_panel,
        )

    @classmethod
    def comments(cls, data: t.List[SimpleNamespace]):
        panels: t.List[Panel] = []

        for item in data:
            panel = cls.comment(data=item, print_panel=False)

            if panel is not None:
                panels.append(panel)

        panel_group = Group(*panels)
        console.print(panel_group)

    @classmethod
    def post(
        cls, data: SimpleNamespace, print_panel: bool = True
    ) -> t.Union[Panel, None]:
        """Render a single Reddit post or comment into a Panel."""

        post = getattr(data, "data", None)
        if not post or not cls.has_attrs(
            obj=post,
            attrs=[
                "title",
                "selftext",
                "author",
                "created",
                "ups",
                "downs",
                "num_comments",
                "all_awardings",
            ],
        ):
            return None

        panel_parts: t.List[str] = []
        subreddit_name = (
            f"self"
            if post.subreddit_name_prefixed.lower() == f"u/{post.author.lower()}"
            else post.subreddit_name_prefixed
        )
        if post.title:
            panel_parts.append(f"**{post.title}**")

        if post.selftext:
            panel_parts.append(post.selftext)

        text: str = "\n\n".join(panel_parts)

        header_content: str = (
            f"{colours.BOLD}{subreddit_name}{colours.RESET} · "
            f"{colours.BOLD_BLUE} [link={post.url}]View on Reddit[/link]"
            f"{colours.BOLD_BLUE_RESET}\nu/{post.author} · "
            f"{colours.BOLD_BLACK}{cls.timestamp_to_relative(unix_timestamp=post.created)}"
            f"{colours.BOLD_BLACK_RESET}"
        )

        footer_content: str = (
            f"{colours.ORANGE_RED}🡅{post.ups}{colours.RESET} "
            f"{colours.SOFT_BLUE}🡇{post.downs}{colours.RESET} "
            f"{colours.WHITE}🗩 {post.num_comments}{colours.WHITE_RESET} "
            f"{colours.BOLD_YELLOW}🎖{len(post.all_awardings)}{colours.BOLD_YELLOW_RESET}"
        )

        if post.over_18:
            header_content = (
                f"{colours.BOLD_RED}NSFW{colours.BOLD_RED_RESET} · {header_content}"
            )

        return cls.panel(
            header=header_content,
            content=text,
            footer=footer_content,
            add_dividers=True,
            print_panel=print_panel,
        )

    @classmethod
    def posts(cls, data: t.List[SimpleNamespace]):
        """Render and print a list of posts/comments using the `post` method."""
        panels: t.List[Panel] = []

        for item in data:
            panel = cls.post(data=item, print_panel=False)
            if panel is not None:
                panels.append(panel)

        panel_group = Group(*panels)
        console.print(panel_group)

    @classmethod
    def subreddit(
        cls, data: SimpleNamespace, print_panel: bool = True
    ) -> t.Union[Panel, None]:
        if data.subreddit_type == "private":
            return None

        panel_parts: t.List[str] = []

        if data.public_description:
            panel_parts.append(f"**{data.public_description}**")
        if data.description:
            panel_parts.append(data.description)

        content = "\n\n".join(panel_parts)

        header_content = (
            f"{colours.BOLD}{data.display_name_prefixed}{colours.RESET} · "
            f"{colours.BOLD_BLACK}{cls.timestamp_to_relative(unix_timestamp=data.created)}"
            f"{colours.BOLD_BLACK_RESET}"
        )

        if data.over18:
            header_content = (
                f"{colours.BOLD_RED}NSFW{colours.BOLD_RED_RESET} · {header_content}"
            )

        footer_data = {"Suscribers": data.subscribers, "Language": data.lang}
        if getattr(data, "accounts_active", None):
            footer_data.update({"Active Accounts": data.accounts_active})

        footer_content = cls.footer_table(footer_data=footer_data)

        return cls.panel(
            header=header_content,
            content=content,
            footer=footer_content,
            add_dividers=True,
            print_panel=print_panel,
        )

    @classmethod
    def subreddits(cls, data: t.List[SimpleNamespace]):
        panels = []
        for item in data:
            subreddit = item.data
            panel = cls.subreddit(data=subreddit, print_panel=False)
            if panel:
                panels.append(panel)

        panels_group = Group(*panels)
        console.print(panels_group)

    @classmethod
    def panel(
        cls,
        content: t.Union[str, RenderableType],
        footer: t.Union[str, Table],
        header: t.Optional[str] = None,
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

            if isinstance(footer, Text) or hasattr(footer, "__rich_console__"):
                # Already a renderable, just use it
                footer_renderable = footer
            else:
                # Fallback to interpreting it as markup text
                footer_renderable = Text.from_markup(
                    str(footer), justify="left", overflow="ellipsis"
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
            bar = "=" * bar_length  # █
            table.add_row(f"[bold]{label}[/bold]", f"{bar} {value}")

        subtitle = f"{x_label} vs {y_label}" if x_label and y_label else ""
        panel = Panel(
            table, title=f"[bold magenta]{title}[/bold magenta]", subtitle=subtitle
        )
        console.print(panel)
