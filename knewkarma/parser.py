import argparse

from rich.markdown import Markdown
from rich_argparse import RichHelpFormatter

from . import DATA_SORT_LISTINGS, POST_LISTINGS


def create_parser() -> argparse.ArgumentParser:
    """
    Creates and configures an argument parser for the command line arguments.

    :return: A configured argparse.ArgumentParser object ready to parse the command line arguments.
    """
    from . import (
        __description__,
        __epilog__,
        __post_examples__,
        __posts_examples__,
        __search_examples__,
        __user_examples__,
        __subreddit_examples__,
        __operations_description__,
        __version__,
    )

    parser = argparse.ArgumentParser(
        description=Markdown(__description__, style="argparse.text"),
        epilog=Markdown(__epilog__, style="argparse.text"),
        formatter_class=RichHelpFormatter,
    )

    subparsers = parser.add_subparsers(
        dest="mode", help="Operation mode", required=False
    )

    # User mode
    user_parser = subparsers.add_parser(
        "user",
        help="User operations",
        description=Markdown(
            __operations_description__.format("User"), style="argparse.text"
        ),
        epilog=Markdown(__user_examples__),
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

    # Subreddit mode
    subreddit_parser = subparsers.add_parser(
        "subreddit",
        help="Subreddit operations",
        description=Markdown(
            __operations_description__.format("Subreddit"), style="argparse.text"
        ),
        epilog=Markdown(__subreddit_examples__),
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

    # Post mode
    post_parser = subparsers.add_parser(
        "post",
        help="Post operations",
        description=Markdown(
            __operations_description__.format("Post"), style="argparse.text"
        ),
        epilog=Markdown(__post_examples__),
        formatter_class=RichHelpFormatter,
    )
    post_parser.add_argument("post_id", help="Post ID")
    post_parser.add_argument("post_subreddit", help="Source subreddit")
    post_parser.add_argument(
        "-p",
        "--profile",
        action="store_true",
        help="Get post profile ([italic][green]default execution[/][/])",
    )
    post_parser.add_argument(
        "-c",
        "--comments",
        dest="show_comments",
        action="store_true",
        help="Show post comments",
    )

    # Posts mode
    posts_parser = subparsers.add_parser(
        "posts",
        help="Posts operations",
        description=Markdown(
            __operations_description__.format("Posts"), style="argparse.text"
        ),
        epilog=Markdown(__posts_examples__),
        formatter_class=RichHelpFormatter,
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
        help="Get posts from a specified listing",
        choices=POST_LISTINGS,
    )

    # Search mode
    search_parser = subparsers.add_parser(
        "search",
        help="Search posts",
        description=Markdown(
            __operations_description__.format("Search"), style="argparse.text"
        ),
        epilog=Markdown(__search_examples__),
        formatter_class=RichHelpFormatter,
    )
    search_parser.add_argument("query", help="Search query")

    # Global options
    parser.add_argument(
        "-s",
        "--sort",
        default="all",
        choices=DATA_SORT_LISTINGS,
        help="Bulk data sort criterion (default: %(default)s)",
    )
    parser.add_argument(
        "-l",
        "--limit",
        default=50,
        type=int,
        help="Maximum number of bulk data to get (default: %(default)s)",
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
        version=__version__,
        action="version",
    )

    return parser
