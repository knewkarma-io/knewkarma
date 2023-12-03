# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

import argparse
import asyncio
import os
from datetime import datetime

import aiohttp
from rich.pretty import pprint

from ._coreutils import log, save_data, pathfinder
from ._parser import create_parser, version
from ._project import PROGRAM_DIRECTORY
from .api import get_updates
from .base import RedditUser, RedditSub, RedditPosts


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


async def setup_cli(arguments: argparse.Namespace):
    """
    Sets up the command-line interface and executes the specified actions.

    :param arguments: Argparse namespace object  containing parsed command-line arguments.
    """
    # -------------------------------------------------------------------- #

    data_timeframe: str = arguments.timeframe
    data_sorting: str = arguments.limit
    data_limit: int = arguments.limit

    # -------------------------------------------------------------------- #

    user = RedditUser(
        username=arguments.username if hasattr(arguments, "username") else None,
        data_timeframe=data_timeframe,
        data_sort=data_sorting,
        data_limit=data_limit,
    )
    subreddit = RedditSub(
        subreddit=arguments.subreddit if hasattr(arguments, "subreddit") else None,
        data_timeframe=data_timeframe,
        data_sort=data_sorting,
        data_limit=data_limit,
    )
    posts = RedditPosts(
        timeframe=data_timeframe,
        sort=data_sorting,
        limit=data_limit,
    )

    # -------------------------------------------------------------------- #

    # Mapping of command-line commands to their respective functions
    function_mapping: dict = {
        "user": [
            ("profile", lambda session: user.profile(session=session)),
            ("posts", lambda session: user.posts(session=session)),
            ("comments", lambda session: user.comments(session=session)),
        ],
        "subreddit": [
            ("profile", lambda session: subreddit.profile(session=session)),
            ("posts", lambda session: subreddit.posts(session=session)),
        ],
        "posts": [
            ("front_page", lambda session: posts.front_page(session=session)),
            (
                "search",
                lambda session: posts.search(query=arguments.search, session=session),
            ),
            (
                "listing",
                lambda session: posts.listing(
                    listings_name=arguments.listing, session=session
                ),
            ),
        ],
    }

    # -------------------------------------------------------------------- #

    if arguments.mode in function_mapping:
        async with aiohttp.ClientSession() as request_session:
            await get_updates(session=request_session)

            mode_action = function_mapping.get(arguments.mode)
            is_executed: bool = False

            for action, function in mode_action:
                if getattr(arguments, action, False):
                    call_function = await function(session=request_session)

                    pprint(call_function, expand_all=True)
                    is_executed = True

                    # -------------------------------------------------------------------- #

                    if arguments.csv or arguments.json:
                        target_directory: str = os.path.join(
                            PROGRAM_DIRECTORY, f"{arguments.mode}_{action}"
                        )
                        pathfinder(
                            directories=[
                                os.path.join(target_directory, "csv"),
                                os.path.join(target_directory, "json"),
                            ]
                        )
                        save_data(
                            data=call_function,
                            save_to_dir=target_directory,
                            save_json=arguments.json,
                            save_csv=arguments.csv,
                        )

                    # -------------------------------------------------------------------- #

            if not is_executed:
                log.warning(
                    f"knewkarma {arguments.mode}: missing one or more expected argument(s)."
                )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def execute_cli():
    """Main entrypoint for the Knew Karma command-line interface."""

    # -------------------------------------------------------------------- #

    parser = create_parser()
    arguments: argparse = parser.parse_args()
    start_time: datetime = datetime.now()

    # -------------------------------------------------------------------- #

    if arguments.mode:
        print(
            """
┓┏┓         ┓┏┓         
┃┫ ┏┓┏┓┓┏┏  ┃┫ ┏┓┏┓┏┳┓┏┓
┛┗┛┛┗┗ ┗┻┛  ┛┗┛┗┻┛ ┛┗┗┗┻"""
        )

        # -------------------------------------------------------------------- #

        try:
            start_time: datetime = datetime.now()

            log.info(
                f"[bold]Knew Karma CLI[/] {version} started at "
                f"{start_time.strftime('%a %b %d %Y, %I:%M:%S%p')}..."
            )
            asyncio.run(setup_cli(arguments=arguments))
        except KeyboardInterrupt:
            log.warning(f"User interruption detected ([yellow]Ctrl+C[/])")
        finally:
            log.info(f"Stopped in {datetime.now() - start_time} seconds.")

        # -------------------------------------------------------------------- #

    else:
        # Display usage information if no mode is provided
        parser.print_usage()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
