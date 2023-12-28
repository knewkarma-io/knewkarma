# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

import argparse
from typing import get_args

from rich.markdown import Markdown
from rich_argparse import RichHelpFormatter

from .info import (
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
    search_examples,
    communities_examples,
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
    subparsers = parser.add_subparsers(dest="mode", help="operation mode")
    parser.add_argument(
        "-u",
        "--updates",
        help="check for updates on run",
        action="store_true",
    )
    parser.add_argument(
        "-l",
        "--limit",
        type=int,
        default=100,
        metavar="NUMBER",
        help="([bold][green]bulk[/][/]) data output limit (default: %(default)s)",
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

    community_parser = subparsers.add_parser(
        "community",
        help="community operations",
        description=Markdown(
            operations_description.format("Community"), style="argparse.text"
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
        help="get a community's profile",
        action="store_true",
    )
    community_parser.add_argument(
        "-pp",
        "--posts",
        help="get a community's posts",
        action="store_true",
    )
    community_parser.add_argument(
        "-r",
        "--rules",
        help="get a community's posts",
        action="store_true",
    )
    community_parser.add_argument(
        "-wp",
        "--wiki-page",
        dest="wiki_page",
        help="get a community's specified wiki page data",
        metavar="WIKI_PAGE",
    )
    community_parser.add_argument(
        "-wps",
        "--wiki-pages",
        dest="wiki_pages",
        help="get a community's wiki pages",
        action="store_true",
    )

    # -------------------------------------------------------------------- #

    communities_parser = subparsers.add_parser(
        "communities",
        help="communities operations",
        description=Markdown(
            operations_description.format("Communities"), style="argparse.text"
        ),
        epilog=Markdown(communities_examples),
        formatter_class=RichHelpFormatter,
    )
    communities_parser.add_argument(
        "-a",
        "--all",
        help="get all communities",
        action="store_true",
    )
    communities_parser.add_argument(
        "-d",
        "--default",
        help="get default communities",
        action="store_true",
    )
    communities_parser.add_argument(
        "-n",
        "--new",
        help="get new communities",
        action="store_true",
    )
    communities_parser.add_argument(
        "-p",
        "--popular",
        help="get popular communities",
        action="store_true",
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

    # -------------------------------------------------------------------- #

    search_parser = subparsers.add_parser(
        "search",
        help="search operations",
        description=Markdown(
            operations_description.format("Search"), style="argparse.text"
        ),
        epilog=Markdown(search_examples),
        formatter_class=RichHelpFormatter,
    )
    search_parser.add_argument("query", help="search query")
    search_parser.add_argument(
        "-u", "--users", help="search users", action="store_true"
    )
    search_parser.add_argument(
        "-p", "--posts", help="search posts", action="store_true"
    )
    search_parser.add_argument(
        "-c", "--communities", help="search communities", action="store_true"
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

    return parser


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
