import typing as t
from datetime import datetime, timezone

from rich.console import RenderableType, Group
from rich.markdown import Markdown
from rich.markup import escape
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

from engines.karmakaze.schemas import (
    User,
    Subreddit,
    WikiPage,
    Comment,
    Post,
    ModeratedSubreddit,
)
from engines.snoopy.reddit import Reddit
from tools import colours
from tools.log_config import console

__all__ = ["RichRender"]


class RichRender:

    @classmethod
    def panels(
        cls,
        data: t.Union[
            t.List[t.Union[User, Post, Subreddit, Comment, WikiPage]],
            User,
            Post,
            Subreddit,
            Comment,
            WikiPage,
        ],
    ):
        """
        Dynamically dispatch the appropriate rendering method based on data type.
        """
        # Handle list input
        if isinstance(data, list) and data:
            item = data[0]
            if isinstance(item, Post):
                return cls._posts(data)
            elif isinstance(item, Comment):
                return cls._comments(data)
            elif isinstance(item, User):
                return cls._users(data)
            elif isinstance(item, (Subreddit, ModeratedSubreddit)):
                return cls._subreddits(data)
            # elif isinstance(item, WikiPage):
            #    return cls.wiki_pages(data)

        # Handle single item input
        elif isinstance(data, Post):
            return cls._post(data)
        elif isinstance(data, Comment):
            return cls._comment(data)
        elif isinstance(data, User):
            return cls._user(data)
        elif isinstance(data, (Subreddit, ModeratedSubreddit)):
            return cls._subreddit(data)
        # elif isinstance(data, WikiPage):
        #    return cls.wiki_page(data)

        console.print(
            "[bold red]Unable to determine render type for the given data.[/]"
        )
        return None

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

    @classmethod
    def _footer_table(cls, footer_data: t.Dict) -> t.Union[Table, None]:
        if footer_data:
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

        return None

    @classmethod
    def _timestamp_to_relative(cls, unix_timestamp: float) -> str:
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
    def _number_to_relative(cls, number: t.Union[int, float]):
        """
        Format a number using abbreviations like k, M, B, etc.
        """
        if number >= 1_000_000_000_000:
            return f"{number / 1_000_000_000_000:.1f}T"
        if number >= 1_000_000_000:
            return f"{number / 1_000_000_000:.1f}B"
        elif number >= 1_000_000:
            return f"{number / 1_000_000:.1f}M"
        elif number >= 1_000:
            return f"{number / 1_000:.1f}K"
        else:
            return str(number)

    @classmethod
    def _user(cls, data: User, print_panel: bool = True):
        subreddit = getattr(data, "subreddit")
        is_suspended = getattr(data, "is_suspended")
        if not is_suspended:

            header_content = (
                f"{colours.BOLD}{colours.POWDER_BLUE}{data.name}{colours.RESET}{colours.RESET} "
                f"· {colours.GREY}{cls._timestamp_to_relative(unix_timestamp=0 if is_suspended else data.created
    )}\n"
                f"{subreddit.display_name_prefixed}{colours.RESET}"
            )

            if is_suspended:
                header_content = f"{colours.BOLD_YELLOW}SUSPENDED{colours.BOLD_YELLOW_RESET} · {header_content}"

            if subreddit.over_18:
                header_content = (
                    f"{colours.BOLD_RED}NSFW{colours.BOLD_RED_RESET} · {header_content}"
                )

            footer_data = {
                "Post Karma": cls._number_to_relative(
                    number=0 if is_suspended else data.link_karma
                ),
                "Comment Karma": cls._number_to_relative(
                    number=0 if is_suspended else data.comment_karma
                ),
                "Total Karma": cls._number_to_relative(
                    number=0 if is_suspended else data.link_karma + data.comment_karma
                ),
            }

            footer_content = cls._footer_table(footer_data=footer_data)

            panel_parts = []
            if subreddit.public_description:
                panel_parts.append(subreddit.public_description)

            text = "\n\n".join(panel_parts)

            return cls._panel(
                title=f"{colours.BOLD_BLUE}[link={Reddit.BASE_URL}{subreddit.url}]View on Reddit[/link]{colours.BOLD_BLUE_RESET}",
                header=header_content,
                content=text,
                footer=footer_content,
                add_dividers=True,
                print_panel=print_panel,
            )

        return None

    @classmethod
    def _users(cls, data: t.List[User], print_panel: bool = True):
        panels = []

        for user_data in data:
            panel = cls._user(user_data, print_panel=print_panel)
            if panel is not None:
                panels.append(panel)

        if panels:
            panel_group = Group(*panels)
            console.print(panel_group)
        else:
            console.print("[dim]No valid users to display.[/]")

    @classmethod
    def _comment(cls, data: Comment, print_panel: bool = True):
        panel_parts: t.List[str] = []

        author: str = getattr(data, "author")
        body: str = getattr(data, "body")
        subreddit: str = getattr(data, "subreddit_name_prefixed", "")
        subreddit = f"self" if subreddit.lower() == f"u/{author.lower()}" else subreddit
        permalink: str = getattr(data, "permalink", "")
        created: int = 0 if getattr(data, "created", None) is None else data.created
        score = cls._number_to_relative(number=data.score)
        _replies = getattr(data.replies, "data")
        num_replies = len(_replies.get("children"))
        awards: list = getattr(data, "all_awardings", [])

        if body:
            panel_parts.append(body)

        text: str = "\n\n".join(panel_parts)
        header_content: str = (
            f"{colours.BOLD}{colours.POWDER_BLUE}{subreddit}{colours.RESET}{colours.RESET} · "
            f"{colours.GREY}{cls._timestamp_to_relative(unix_timestamp=created)}\n"
            f"u/{escape(author)}{colours.RESET}"
        )

        footer_content: str = (
            f"{colours.ORANGE_RED}🡅{colours.RESET} {"[dim]" 
            if score == 0 
            else colours.POWDER_BLUE}{score}{colours.RESET} {colours.SOFT_BLUE}🡇{colours.RESET} "
            f"💬{colours.POWDER_BLUE}{cls._number_to_relative(number=num_replies)}{colours.RESET} "
            f"{colours.BOLD_YELLOW}🏆{cls._number_to_relative(number=len(awards))}{colours.BOLD_YELLOW_RESET}"
        )

        return cls._panel(
            title=f"{colours.BOLD_BLUE}[link={Reddit.BASE_URL}/{permalink}]View on Reddit[/link]{colours.BOLD_BLUE_RESET}",
            header=header_content,
            content=text,
            footer=footer_content,
            add_dividers=True,
            print_panel=print_panel,
        )

    @classmethod
    def _comments(cls, data: t.List[Comment]):
        panels: t.List[Panel] = []

        for item in data:
            panel = cls._comment(data=item, print_panel=False)

            if panel is not None:
                panels.append(panel)

        panel_group = Group(*panels)
        console.print(panel_group)

    @classmethod
    def _post(cls, data: Post, print_panel: bool = True) -> t.Union[Panel, None]:
        """Render a single Reddit post or comment into a Panel."""

        panel_parts: t.List[str] = []
        subreddit_name = (
            f"self"
            if data.subreddit_name_prefixed.lower() == f"u/{data.author.lower()}"
            else data.subreddit_name_prefixed
        )
        if data.title:
            panel_parts.append(f"**{data.title}**")

        if data.selftext:
            panel_parts.append(data.selftext)

        text: str = "\n\n".join(panel_parts)

        score = cls._number_to_relative(number=data.score)
        header_content: str = (
            f"{colours.BOLD}{colours.POWDER_BLUE}{subreddit_name}{colours.RESET}{colours.RESET} · "
            f"{colours.GREY}{cls._timestamp_to_relative(unix_timestamp=0 if getattr(data, "created", None) 
                                                                            is None else data.created)}{colours.RESET}\n"
            f"{colours.GREY}u/{data.author}{colours.RESET}"
        )

        footer_content: str = (
            f"{colours.ORANGE_RED}🡅{colours.RESET} {"[dim]" 
            if score == 0 
            else colours.POWDER_BLUE}{score}{colours.RESET} {colours.SOFT_BLUE}🡇{colours.RESET} "
            f"💬{colours.POWDER_BLUE}{cls._number_to_relative(number=data.num_comments)}{colours.RESET} "
            f"{colours.BOLD_YELLOW}🏆{cls._number_to_relative(number=len(data.all_awardings))}{colours.BOLD_YELLOW_RESET}"
        )

        if data.over_18:
            header_content = (
                f"{colours.BOLD_RED}NSFW{colours.BOLD_RED_RESET} · {header_content}"
            )

        return cls._panel(
            title=f"{colours.BOLD_BLUE}[link={data.url}]View on Reddit[/link]{colours.BOLD_BLUE_RESET}",
            header=header_content,
            content=text,
            footer=footer_content,
            add_dividers=True,
            print_panel=print_panel,
        )

    @classmethod
    def _posts(cls, data: t.List[Post]):
        """Render and print a list of posts/comments using the `post` method."""
        panels: t.List[Panel] = []

        for item in data:
            panel = cls._post(data=item, print_panel=False)
            if panel is not None:
                panels.append(panel)

        panel_group = Group(*panels)
        console.print(panel_group)

    @classmethod
    def _subreddit(
        cls, data: t.Union[Subreddit, ModeratedSubreddit], print_panel: bool = True
    ) -> t.Union[Panel, None]:
        if data.subreddit_type == "private":
            return None

        has_public_description: bool = hasattr(data, "public_description")
        has_description: bool = hasattr(data, "description")
        is_nsfw: bool = (
            getattr(data, "over_18")
            if hasattr(data, "over_18")
            else getattr(data, "over18")
        )
        has_title = hasattr(data, "title")

        panel_parts: t.List[str] = []

        if has_title:
            panel_parts.append(f"**{data.title}**")
        if has_public_description:
            panel_parts.append(f"**{data.public_description}**")
        if has_description:
            panel_parts.append(data.description)

        content: str = "\n\n".join(panel_parts)

        header_content: str = (
            f"{colours.BOLD}{data.display_name_prefixed}{colours.RESET} · "
            f"{colours.BOLD_BLACK}{cls._timestamp_to_relative(unix_timestamp=0 if getattr(data, "created", None) is None else data.created
)}"
            f"{colours.BOLD_BLACK_RESET}"
        )

        if is_nsfw:
            header_content: str = (
                f"{colours.BOLD_RED}NSFW{colours.BOLD_RED_RESET} · {header_content}"
            )

        footer_data: t.Union[t.Dict, None] = {
            "Subscribers": cls._number_to_relative(number=data.subscribers)
        }
        if getattr(data, "accounts_active", None):
            footer_data.update(
                {
                    "Active Accounts": cls._number_to_relative(
                        number=data.accounts_active
                    )
                }
            )
        if hasattr(data, "lang"):
            footer_data.update({"Language": data.lang})

        if data.subreddit_type == "user":
            footer_data = None

        footer_content = cls._footer_table(footer_data=footer_data)

        return cls._panel(
            header=header_content,
            content=content,
            footer=footer_content,
            add_dividers=True,
            print_panel=print_panel,
        )

    @classmethod
    def _subreddits(cls, data: t.List[t.Union[Subreddit, ModeratedSubreddit]]):
        panels = []
        for subreddit in data:
            panel = cls._subreddit(data=subreddit, print_panel=False)
            if panel:
                panels.append(panel)

        panels_group = Group(*panels)
        console.print(panels_group)

    @classmethod
    def _panel(
        cls,
        content: t.Union[str, RenderableType],
        title: t.Union[str, None] = None,
        footer: t.Union[str, Table, None] = None,
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
            content_renderable = Markdown(content, justify="left")
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
            title=title,
            title_align="right",
            renderable=group,
            border_style="#444444" if show_outline else "black",
        )

        if print_panel:
            console.print(panel)

        return panel
