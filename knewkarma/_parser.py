# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

import argparse

from rich.markdown import Markdown
from rich_argparse import RichHelpFormatter

from ._metadata import (
    version,
    description,
    epilog,
    posts_examples,
    user_examples,
    subreddit_examples,
    operations_description,
)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def create_parser() -> argparse.ArgumentParser:
    """
    Creates and configures an argument parser for the command line arguments.

    :return: A configured argparse.ArgumentParser object ready to parse the command line arguments.
    """

    parser = argparse.ArgumentParser(
        description=Markdown(description, style="argparse.text"),
        epilog=Markdown(epilog, style="argparse.text"),
        formatter_class=RichHelpFormatter,
    )
    parser.add_argument(
        "--runtime-prof",
        dest="runtime_profiler",
        help="([bold][green]dev[/][/]) enable runtime profiler.",
        action="store_true",
    )
    parser.add_argument(
        "-pct",
        "--prof-clock-type",
        dest="prof_clock_type",
        help="set profiler clock type (default: %(default)s)",
        default="CPU",
        choices=["WALL", "CPU"],
    )
    parser.add_argument(
        "-pss",
        "--prof-stats-sort",
        dest="prof_stats_sort",
        help="profiler stats sort criterion (default: %(default)s)",
        default="ncall",
        choices=[
            "ttot",
            "tsub",
            "tavg",
            "ncall",
            "name",
            "lineno",
            "builtin",
            "threadid",
            "tt_perc",
            "tsub_perc",
        ],
    )
    subparsers = parser.add_subparsers(
        dest="mode", help="Operation mode", required=False
    )

    # User parser
    user_parser = subparsers.add_parser(
        "user",
        help="User operations",
        description=Markdown(
            operations_description.format("User"), style="argparse.text"
        ),
        epilog=Markdown(user_examples),
        formatter_class=RichHelpFormatter,
    )
    user_parser.add_argument("username", help="Username to query")
    user_parser.add_argument(
        "-p",
        "--profile",
        action="store_true",
        help="Get user profile ([italic][green]default execution[/][/])",
    )
    user_parser.add_argument(
        "-c",
        "--comments",
        action="store_true",
        help="Get user comments",
    )
    user_parser.add_argument(
        "-pp", "--posts", action="store_true", help="Get user posts"
    )

    # Subreddit parser
    subreddit_parser = subparsers.add_parser(
        "subreddit",
        help="Subreddit operations",
        description=Markdown(
            operations_description.format("Subreddit"), style="argparse.text"
        ),
        epilog=Markdown(subreddit_examples),
        formatter_class=RichHelpFormatter,
    )
    subreddit_parser.add_argument(
        "subreddit",
        help="Subreddit to query",
    )
    subreddit_parser.add_argument(
        "-p",
        "--profile",
        action="store_true",
        help="Get subreddit profile ([italic][green]default execution[/][/])",
    )
    subreddit_parser.add_argument(
        "-pp",
        "--posts",
        action="store_true",
        help="Get subreddit posts",
    )

    # Posts parser
    posts_parser = subparsers.add_parser(
        "posts",
        help="Posts operations",
        description=Markdown(
            operations_description.format("Posts"), style="argparse.text"
        ),
        epilog=Markdown(posts_examples),
        formatter_class=RichHelpFormatter,
    )
    posts_parser.add_argument(
        "-s",
        "--search",
        help="Search posts",
    )
    posts_parser.add_argument(
        "-f",
        "--front-page",
        help="Get posts from Reddit Front-Page ([italic][green]default execution[/][/])",
        action="store_true",
    )
    posts_parser.add_argument(
        "-l",
        "--listing",
        default="all",
        help="Get posts from a specified listing",
        choices=["best", "controversial", "popular", "rising"],
    )

    # Global parser
    parser.add_argument(
        "-s",
        "--sort",
        type=str,
        default="all",
        choices=[
            "controversial",
            "new",
            "top",
            "best",
            "hot",
            "rising",
        ],
        help="Bulk data sort criterion",
    )
    parser.add_argument(
        "-l",
        "--limit",
        type=int,
        default=100,
        help="Bulk data output limit",
    )
    parser.add_argument(
        "-j",
        "--json",
        help="Write data to a JSON file.",
        action="store_true",
    )
    parser.add_argument(
        "-c",
        "--csv",
        help="Write data to a CSV file.",
        action="store_true",
    )
    parser.add_argument(
        "-d",
        "--debug",
        help="Run Knew Karma in debug mode.",
        action="store_true",
    )
    parser.add_argument(
        "-v",
        "--version",
        version=version,
        action="version",
    )

    return parser


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
