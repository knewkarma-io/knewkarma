import argparse
import csv
import json
import logging
import os
from datetime import datetime
from typing import Union

from rich.markdown import Markdown
from rich_argparse import RichHelpFormatter

from . import CSV_DIRECTORY, JSON_DIRECTORY
from . import DATA_SORT_CRITERION, POST_LISTINGS


def create_parser() -> argparse.ArgumentParser:
    """
    Creates and configures an argument parser for the command line arguments.

    :return: A configured argparse.ArgumentParser object ready to parse the command line arguments.
    """
    from . import (
        __description__,
        __epilog__,
        __post_example__,
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
        epilog=Markdown(__post_example__),
        formatter_class=RichHelpFormatter,
    )
    post_parser.add_argument("post_id", help="Post ID")
    post_parser.add_argument("post_subreddit", help="Source subreddit")

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
        dest="sort_criterion",
        choices=DATA_SORT_CRITERION,
        help="Bulk data sort criterion",
    )
    parser.add_argument(
        "-l",
        "--limit",
        dest="data_limit",
        type=int,
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
        version=__version__,
        action="version",
    )

    return parser


def convert_timestamp_to_datetime(timestamp: float) -> str:
    """
    Converts a Unix timestamp to a formatted datetime string.

    :param timestamp: The Unix timestamp to be converted.
    :return: A formatted datetime string in the format "dd MMMM yyyy, hh:mm:ssAM/PM".
    """
    utc_from_timestamp: datetime = datetime.fromtimestamp(timestamp)
    datetime_object: utc_from_timestamp = utc_from_timestamp.strftime(
        "%d %B %Y, %I:%M:%S%p"
    )
    return datetime_object


def data_broker(api_data: dict, data_file: str) -> dict:
    """
    Re-formats API data based on a key mapping from a JSON file.

    :param api_data: A JSON object containing raw data from the API.
    :param data_file: Path to the JSON file that contains the key mapping.

    :returns: A re-formatted JSON object with human-readable keys.
    """
    from . import CURRENT_FILE_DIRECTORY

    # Construct path to the mapping data file
    mapping_data_file: str = os.path.join(CURRENT_FILE_DIRECTORY, "data", data_file)

    # Load the mapping from the specified file
    with open(mapping_data_file, "r", encoding="utf-8") as file:
        mapping_data: dict = json.load(file)

    # Initialize an empty dictionary to hold the formatted data
    formatted_data = {}

    # Map API data to human-readable format using the mapping
    for api_data_key, mapping_data_key in mapping_data.items():
        formatted_data[mapping_data_key]: dict = api_data.get(api_data_key, "N/A")

    return formatted_data


def path_finder():
    """
    Creates file directories if they don't already exist.
    """
    file_directories: list = [CSV_DIRECTORY, JSON_DIRECTORY]
    for directory in file_directories:
        os.makedirs(directory, exist_ok=True)


def save_data(
        data: Union[dict, list],
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
    # Save to JSON if save_json is True
    if save_to_json:
        with open(os.path.join(JSON_DIRECTORY, f"{filename}.json"), "w") as json_file:
            json.dump(data, json_file, indent=4)
        log.info(f"JSON data saved to [link file://{json_file.name}]{json_file.name}")

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
        log.info(f"CSV data saved to [link file://{csv_file.name}]{csv_file.name}")


def setup_logging(debug_mode: bool) -> logging.getLogger:
    """
    Configure and return a logging object with the specified log level.

    :param debug_mode: A boolean value indicating whether log level should be set to DEBUG.
    :return: A logging object configured with the specified log level.
    """
    from rich.logging import RichHandler

    logging.basicConfig(
        level="NOTSET" if debug_mode else "INFO",
        format="%(message)s",
        handlers=[
            RichHandler(
                markup=True, log_time_format="[%I:%M:%S %p]", show_level=debug_mode
            )
        ],
    )
    return logging.getLogger("Knew Karma")


arguments: argparse = create_parser().parse_args()
log: logging = setup_logging(debug_mode=arguments.debug)
