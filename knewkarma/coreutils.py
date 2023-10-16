import argparse
import json
import logging
import os
from datetime import datetime

from rich import print
from rich.logging import RichHandler
from rich.markdown import Markdown

from . import __version__, __author__, __about__


def banner() -> str:
    return f"""
┓┏┓         ┓┏┓         
┃┫ ┏┓┏┓┓┏┏  ┃┫ ┏┓┏┓┏┳┓┏┓
┛┗┛┛┗┗ ┗┻┛  ┛┗┛┗┻┛ ┛┗┗┗┻v{__version__}"""


def format_api_data(api_data: dict, data_file: str) -> dict:
    """
    Formats API data based on a key mapping from a JSON file.

    :param api_data: Dictionary containing raw data from the API.
    :param data_file: Path to the JSON file that contains the key mapping.

    :returns: A Formatted JSON object with human-readable keys.
    """

    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the settings.json file
    data = os.path.join(current_dir, "data", data_file)

    # Load the mapping from the specified file
    with open(data, "r") as file:
        key_mapping = json.load(file)

    # Initialize an empty dictionary to hold the formatted data
    formatted_data = {}

    # Map API data to human-readable format using the mapping
    for api_key, readable_key in key_mapping.items():
        formatted_data[readable_key] = api_data.get(api_key, "N/A")

    return formatted_data


async def check_updates():
    """
    This function checks if there's a new release of a project on GitHub. If there is, it logs an
    information message and prints the release notes.
    """
    from .api import API

    # Make a GET request to the GitHub API to get the latest release of the project.
    response = await API.get_data(
        endpoint="https://api.github.com/repos/bellingcat/knewkarma/releases/latest"
    )

    if response:
        remote_version = response.get("tag_name")

        # Check if the remote version tag matches the current version tag.
        if remote_version != __version__:
            # If not, convert the release notes from Markdown to HTML.
            raw_release_notes = response.get("body")

            # Log an info message about the new release.
            log.info(
                f"Knew Karma {remote_version} is available. "
                f"Run 'pip install --upgrade knewkarma' to get the updates."
            )

            # Print the release notes.
            print(Markdown(raw_release_notes))


def convert_timestamp_to_datetime(timestamp: int) -> str:
    """
    Converts a Unix timestamp to a formatted datetime string.

    :param timestamp: The Unix timestamp to be converted.
    :return: A formatted datetime string in the format "dd MMMM yyyy, hh:mm:ssAM/PM".
    """
    utc_from_timestamp = datetime.fromtimestamp(timestamp)
    datetime_object = utc_from_timestamp.strftime("%d %B %Y, %I:%M:%S%p")
    return datetime_object


def set_loglevel(debug_mode: bool) -> logging.getLogger:
    """
    Configure and return a logging object with the specified log level.

    :param debug_mode: If True, the log level is set to "NOTSET". Otherwise, it is set to "INFO".
    :return: A logging object configured with the specified log level.
    """
    logging.basicConfig(
        level="NOTSET" if debug_mode else "INFO",
        format="%(message)s",
        handlers=[
            RichHandler(markup=True, log_time_format="%I:%M:%S %p", show_level=False)
        ],
    )
    return logging.getLogger(f"Knew Karma")


def create_parser() -> argparse.ArgumentParser:
    """
    Creates and configures an argument parser for the command line arguments.

    :return: A configured argparse.ArgumentParser object ready to parse the command line arguments.
    """
    parser = argparse.ArgumentParser(
        description=f"Knew Karma - by {__author__} ({__about__})",
        epilog="A Reddit Data Analysis Toolkit.",
    )

    subparsers = parser.add_subparsers(dest="mode", help="Operation mode")

    # User mode
    user_parser = subparsers.add_parser("user", help="User operations")
    user_parser.add_argument(
        "-profile-", dest="profile", action="store_true", help="Get a user's profile"
    )
    user_parser.add_argument(
        "-posts-", dest="posts", action="store_true", help="Get a user's posts"
    )
    user_parser.add_argument(
        "-comments-", dest="comments", action="store_true", help="Get a user's comments"
    )
    user_parser.add_argument("username", help="Username to query")

    # Subreddit mode
    subreddit_parser = subparsers.add_parser("subreddit", help="User operations")
    subreddit_parser.add_argument(
        "-profile-",
        dest="profile",
        action="store_true",
        help="Get a subreddit's profile",
    )
    subreddit_parser.add_argument(
        "-posts-", dest="posts", action="store_true", help="Get a subreddit's posts"
    )
    subreddit_parser.add_argument("subreddit", help="Subreddit to query")

    # Post mode
    post_parser = subparsers.add_parser("post", help="Post operations")
    post_parser.add_argument(
        "-profile-",
        dest="profile",
        action="store_true",
        help="Get a post's (profile) data",
    )
    post_parser.add_argument(
        "-comments-", dest="comments", action="store_true", help="Get a post's comments"
    )
    post_parser.add_argument(
        "-awards-", dest="awards", action="store_true", help=argparse.SUPPRESS
    )
    post_parser.add_argument(
        "id",
        help="Post ID",
    )
    post_parser.add_argument(
        "subreddit",
        help="Source subreddit",
    )

    # Posts mode
    posts_parser = subparsers.add_parser("posts", help="Posts operations")
    posts_parser.add_argument(
        "-listings-",
        dest="listings",
        action="store_true",
        help="Get posts from a specified listing",
    )
    posts_parser.add_argument(
        "-frontpage-",
        dest="frontpage",
        action="store_true",
        help="Get posts from the Reddit front-page",
    )
    posts_parser.add_argument(
        "--listing",
        help="Post listing name",
        choices=["hot", "new", "top"],
        default="all",
    )

    # Search mode
    search_parser = subparsers.add_parser("search", help="Search posts")
    search_parser.add_argument("query", help="Search query")

    # Global options
    parser.add_argument(
        "-s",
        "--sort",
        default="all",
        choices=["controversial", "new", "top", "best", "hot", "rising"],
        help="Data sort criterion (default: new)",
    )
    parser.add_argument(
        "-l",
        "--limit",
        default=100,
        type=int,
        help="Maximum number of posts/comments to get (default: %(default)s)",
    )
    parser.add_argument(
        "--json",
        help="Write all found data to a JSON file.",
        action="store_true",
    )
    parser.add_argument(
        "--csv",
        help="Write all found data to a CSV file.",
        action="store_true",
    )
    parser.add_argument(
        "-d",
        "--debug",
        help="Run in debug mode",
        action="store_true",
    )
    parser.add_argument(
        "-v",
        "--version",
        version=__version__,
        action="version",
    )

    return parser


args = create_parser().parse_args()
log = set_loglevel(debug_mode=args.debug)
