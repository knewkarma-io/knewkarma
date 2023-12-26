# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

import argparse
from typing import get_args

from rich.markdown import Markdown
from rich_argparse import RichHelpFormatter

from ._meta import (
    community_examples,
    description,
    epilog,
    posts_examples,
    user_examples,
    operations_description,
    version,
    POSTS_LISTINGS,
    DATA_TIMEFRAME,
    DATA_SORT_CRITERION,
)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def create_parser() -> argparse.ArgumentParser:
    """
    Creates and configures an argument parser for the command line arguments.

    :return: A configured argparse.ArgumentParser object ready to parse the command line arguments.
    :rtype: argparse.ArgumentParser
    """
    # -------------------------------------------------------------------- #

    parser = argparse.ArgumentParser(
        description=Markdown(description, style="argparse.text"),
        epilog=Markdown(epilog, style="argparse.text"),
        formatter_class=RichHelpFormatter,
    )
    subparsers = parser.add_subparsers(
        dest="mode",
        help="operation mode",
    )
    parser.add_argument(
        "-l",
        "--limit",
        type=int,
        default=100,
        help="([bold][green]bulk[/][/]) data output limit (default: %(default)s)",
    )
    parser.add_argument(
        "-t",
        "--timeframe",
        type=str,
        default="all",
        choices=list(get_args(DATA_TIMEFRAME)),
        help="timeframe to get ([bold][green]bulk[/][/]) data from (default: %(default)s)",
    )
    parser.add_argument(
        "-s",
        "--sort",
        type=str,
        default="all",
        choices=list(get_args(DATA_SORT_CRITERION)),
        help="([bold][green]bulk[/][/]) sort criterion (default: %(default)s)",
    )

    parser.add_argument(
        "-j",
        "--json",
        metavar="FILENAME",
        help="write output to a json file",
    )
    parser.add_argument(
        "-c",
        "--csv",
        metavar="FILENAME",
        help="write output to a csv file",
    )
    parser.add_argument(
        "-d",
        "--debug",
        help="([bold][blue]dev[/][/]) run knew karma in debug mode",
        action="store_true",
    )
    parser.add_argument(
        "-v",
        "--version",
        version=f"Knew Karma {version}",
        action="version",
    )

    # -------------------------------------------------------------------- #

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
        "-c",
        "--comments",
        help="get a user's comments",
        action="store_true",
    )
    user_parser.add_argument(
        "-p",
        "--profile",
        help="get a user's profile",
        action="store_true",
    )

    user_parser.add_argument(
        "-pp",
        "--posts",
        action="store_true",
        help="get a user's posts",
    )
    user_parser.add_argument(
        "-mc",
        "--moderated-communities",
        dest="moderated_communities",
        help="get communities moderated by the user",
        action="store_true",
    )
    user_parser.add_argument(
        "-tc",
        "--top-communities",
        dest="top_communities",
        metavar="TOP_N",
        type=int,
        help="get a user's top n communities based on community frequency in n posts",
    )

    # -------------------------------------------------------------------- #

    community_parser = subparsers.add_parser(
        "community",
        help="community operations",
        description=Markdown(
            operations_description.format("Community/Subreddit"), style="argparse.text"
        ),
        epilog=Markdown(community_examples),
        formatter_class=RichHelpFormatter,
    )
    community_parser.add_argument(
        "community",
        help="community name",
    )
    community_parser.add_argument(
        "-p",
        "--profile",
        action="store_true",
        help="get a community's profile",
    )
    community_parser.add_argument(
        "-pp",
        "--posts",
        action="store_true",
        help="get a community's posts",
    )

    # -------------------------------------------------------------------- #

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
        "-n",
        "--new",
        help="get new posts",
        action="store_true",
    )
    posts_parser.add_argument(
        "-f",
        "--front-page",
        help="get posts from the reddit front-page",
        action="store_true",
    )
    posts_parser.add_argument(
        "-s",
        "--search",
        help="get posts that match a specified search query",
    )
    posts_parser.add_argument(
        "-l",
        "--listing",
        default="all",
        help="get posts from a specified listing",
        choices=list(get_args(POSTS_LISTINGS)),
    )

    return parser


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
