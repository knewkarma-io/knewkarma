import argparse
import csv
import json
import logging
import os
from datetime import datetime

from rich.logging import RichHandler
from rich.markdown import Markdown
from rich_argparse import RichHelpFormatter

from . import __version__, __description__, __epilog__


def path_finder():
    """
    Creates file directories if they don't already exist.
    """
    file_directories = [CSV_DIRECTORY, JSON_DIRECTORY]
    for directory in file_directories:
        os.makedirs(directory, exist_ok=True)


def save_data(
    data: dict,
    filename: str,
    save_to_json: bool = False,
    save_to_csv: bool = False,
):
    """
    Save the given data to JSON and/or CSV files based on the arguments.

    :param data: The data to be saved, which is a list of dictionaries.
    :param filename: The base filename to use when saving.
    :param save_to_json: A boolean value to indicate whether to save data as a JSON file.
    :param save_to_csv: A boolean value to indicate whether to save data as a CSV file.
    """
    from glyphoji import glyph

    # Save to JSON if save_json is True
    if save_to_json:
        with open(os.path.join(JSON_DIRECTORY, f"{filename}.json"), "w") as json_file:
            json.dump(data, json_file)
        log.info(f"JSON data saved to {json_file.name} {glyph.party_popper}")

    # Save to CSV if save_csv is True
    if save_to_csv:
        with open(
            os.path.join(CSV_DIRECTORY, f"{filename}.csv"), "w", newline=""
        ) as csv_file:
            writer = csv.writer(csv_file)
            # Write the header based on keys from the first dictionary
            header = data.keys()
            writer.writerow(header)

            # Write each row
            writer.writerow(data.values())
        log.info(f"CSV data saved to {csv_file.name} {glyph.party_popper}")


def convert_timestamp_to_datetime(timestamp: float) -> str:
    """
    Converts a Unix timestamp to a formatted datetime string.

    :param timestamp: The Unix timestamp to be converted.
    :return: A formatted datetime string in the format "dd MMMM yyyy, hh:mm:ssAM/PM".
    """
    utc_from_timestamp = datetime.fromtimestamp(timestamp)
    datetime_object = utc_from_timestamp.strftime("%d %B %Y, %I:%M:%S%p")
    return datetime_object


def setup_logging(debug_mode: bool) -> logging.getLogger:
    """
    Configure and return a logging object with the specified log level.

    :param debug_mode: A boolean value indicating whether debug mode should be enabled or not.
    :return: A logging object configured with the specified log level.
    """
    logging.basicConfig(
        level="NOTSET" if debug_mode else "INFO",
        format="%(message)s",
        handlers=[
            RichHandler(
                markup=True, log_time_format="%I:%M:%S %p", show_level=debug_mode
            )
        ],
    )
    return logging.getLogger("Knew Karma")


def create_parser() -> argparse.ArgumentParser:
    """
    Creates and configures an argument parser for the command line arguments.

    :return: A configured argparse.ArgumentParser object ready to parse the command line arguments.
    """
    from . import __operations_description__, __operations_epilog__

    parser = argparse.ArgumentParser(
        description=Markdown(__description__, style="argparse.text"),
        epilog=Markdown(__epilog__, style="argparse.text"),
        formatter_class=RichHelpFormatter,
    )

    subparsers = parser.add_subparsers(
        dest="mode", help="Operation mode", required=True
    )

    # User mode
    user_parser = subparsers.add_parser(
        "user",
        help="User operations",
        description=Markdown(
            __operations_description__.format("User"), style="argparse.text"
        ),
        epilog=Markdown(__operations_epilog__.format("user"), style="argparse.text"),
        formatter_class=RichHelpFormatter,
    )
    user_parser.add_argument("username", help="Username to query")
    user_parser.add_argument(
        "-comments-",
        dest="comments",
        action="store_true",
        help="Get a user's comments",
    )
    user_parser.add_argument(
        "-posts-", dest="posts", action="store_true", help="Get a user's posts"
    )
    user_parser.add_argument(
        "-profile-", dest="profile", action="store_true", help="Get a user's profile"
    )

    # Subreddit mode
    subreddit_parser = subparsers.add_parser(
        "subreddit",
        help="Subreddit operations",
        description=Markdown(
            __operations_description__.format("Subreddit"), style="argparse.text"
        ),
        epilog=Markdown(
            __operations_epilog__.format("subreddit"), style="argparse.text"
        ),
        formatter_class=RichHelpFormatter,
    )
    subreddit_parser.add_argument("subreddit", help="Subreddit to query")
    subreddit_parser.add_argument(
        "-profile-",
        dest="profile",
        action="store_true",
        help="Get a subreddit's profile",
    )
    subreddit_parser.add_argument(
        "-posts-",
        dest="posts",
        action="store_true",
        help="Get a subreddit's posts",
    )

    # Post mode
    post_parser = subparsers.add_parser(
        "post",
        help="Post operations",
        description=Markdown(
            __operations_description__.format("Post"), style="argparse.text"
        ),
        epilog=Markdown(__operations_epilog__.format("post"), style="argparse.text"),
        formatter_class=RichHelpFormatter,
    )
    post_parser.add_argument(
        "id",
        help="Post ID",
    )
    post_parser.add_argument(
        "subreddit",
        help="Source subreddit",
    )
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

    # Posts mode
    posts_parser = subparsers.add_parser(
        "posts",
        help="Posts operations",
        description=Markdown(
            __operations_description__.format("Posts"), style="argparse.text"
        ),
        epilog=Markdown(__operations_epilog__.format("posts"), style="argparse.text"),
        formatter_class=RichHelpFormatter,
    )
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
    search_parser = subparsers.add_parser(
        "search",
        help="Search posts",
        description=Markdown(
            __operations_description__.format("Search"), style="argparse.text"
        ),
        epilog=Markdown(__operations_epilog__.format("search"), style="argparse.text"),
        formatter_class=RichHelpFormatter,
    )
    search_parser.add_argument("query", help="Search query")

    # Global options
    parser.add_argument(
        "-s",
        "--sort",
        default="all",
        choices=["controversial", "new", "top", "best", "hot", "rising"],
        help="Bulk data sort criterion (default: %(default)s)",
    )
    parser.add_argument(
        "-l",
        "--limit",
        default=10,
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
        help="Enable debug mode",
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
log = setup_logging(debug_mode=args.debug)

# Construct path to the program's directory
PROGRAM_DIRECTORY = os.path.expanduser(os.path.join("~", "knewkarma"))

# Construct path to the current file's directory
CURRENT_FILE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# Construct paths to directories of CSV and JSON files.
CSV_DIRECTORY = os.path.join(PROGRAM_DIRECTORY, "csv")
JSON_DIRECTORY = os.path.join(PROGRAM_DIRECTORY, "json")
