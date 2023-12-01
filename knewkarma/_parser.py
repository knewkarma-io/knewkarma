# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

import argparse

from rich.markdown import Markdown
from rich_argparse import RichHelpFormatter

from .metadata import (
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
    # ---------------------------------------------------------- #

    parser = argparse.ArgumentParser(
        description=Markdown(description, style="argparse.text"),
        epilog=Markdown(epilog, style="argparse.text"),
        formatter_class=RichHelpFormatter,
    )
    subparsers = parser.add_subparsers(
        dest="mode", help="operation mode", required=False
    )
    parser.add_argument(
        "-l",
        "--limit",
        type=int,
        default=100,
        help="(bulk) data output limit",
    )

    parser.add_argument(
        "-s",
        "--sort",
        type=str,
        default="all",
        choices=[
            "all",
            "best",
            "controversial",
            "hot",
            "new",
            "rising",
            "top",
        ],
        help="(bulk) data sort criterion",
    )

    parser.add_argument(
        "-j",
        "--json",
        help="write output to a specified json file",
    )
    parser.add_argument(
        "-c",
        "--csv",
        help="write output to a specified csv file",
    )
    parser.add_argument(
        "-d",
        "--debug",
        help="([bold][green]dev[/][/]) run knew karma in debug mode.",
        action="store_true",
    )
    parser.add_argument(
        "-v",
        "--version",
        version=f"Knew Karma {version}",
        action="version",
    )

    # ---------------------------------------------------------- #

    user_parser = subparsers.add_parser(
        "user",
        help="user operations",
        description=Markdown(
            operations_description.format("User"), style="argparse.text"
        ),
        epilog=Markdown(user_examples),
        formatter_class=RichHelpFormatter,
    )
    user_parser.add_argument("username", help="username")
    user_parser.add_argument(
        "-p",
        "--profile",
        action="store_true",
        help="get profile from the specified username",
    )
    user_parser.add_argument(
        "-c",
        "--comments",
        action="store_true",
        help="get comments from the specified username",
    )
    user_parser.add_argument(
        "-pp",
        "--posts",
        action="store_true",
        help="get posts from the specified username",
    )

    # ---------------------------------------------------------- #

    subreddit_parser = subparsers.add_parser(
        "subreddit",
        help="subreddit operations",
        description=Markdown(
            operations_description.format("Subreddit"), style="argparse.text"
        ),
        epilog=Markdown(subreddit_examples),
        formatter_class=RichHelpFormatter,
    )
    subreddit_parser.add_argument(
        "subreddit",
        help="subreddit name",
    )
    subreddit_parser.add_argument(
        "-p",
        "--profile",
        action="store_true",
        help="get profile from the specified subreddit",
    )
    subreddit_parser.add_argument(
        "-pp",
        "--posts",
        action="store_true",
        help="get posts from the specified subreddit",
    )

    # ---------------------------------------------------------- #

    posts_parser = subparsers.add_parser(
        "posts",
        help="posts operations",
        description=Markdown(
            operations_description.format("Posts"), style="argparse.text"
        ),
        epilog=Markdown(posts_examples),
        formatter_class=RichHelpFormatter,
    )
    posts_parser.add_argument(
        "-s",
        "--search",
        help="get posts that match a specified search query",
    )
    posts_parser.add_argument(
        "-f",
        "--front-page",
        help="get posts from the reddit front-page",
        action="store_true",
    )
    posts_parser.add_argument(
        "-l",
        "--listing",
        default="all",
        help="get posts from a specified listing",
        choices=["best", "controversial", "popular", "rising"],
    )

    return parser


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
