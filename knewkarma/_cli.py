# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

import argparse
import asyncio
import os
from datetime import datetime

import aiohttp
import rich

from ._meta import PROGRAM_DIRECTORY
from ._parser import create_parser, version
from ._utils import dataframe, log, pathfinder
from .base import RedditUser, RedditCommunity, RedditPosts


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


async def stage_and_execute(arguments: argparse.Namespace):
    """
    Stages the command-line interface and executes command-line arguments based on user-input.

    :param arguments: Argparse namespace object  containing parsed command-line arguments.
    :type arguments: argparse.Namespace
    """

    limit: int = arguments.limit
    sort = arguments.sort
    timeframe = arguments.timeframe

    # ------------------------------------------------------------------------ #

    user = RedditUser(
        username=arguments.username if hasattr(arguments, "username") else None,
    )
    community = RedditCommunity(
        community=arguments.community if hasattr(arguments, "community") else None,
    )
    posts = RedditPosts()

    # ------------------------------------------------------------------------ #

    # Mapping of command-line commands to their respective functions
    function_mapping: dict = {
        "user": [
            ("profile", lambda session: user.profile(session=session)),
            (
                "posts",
                lambda session: user.posts(
                    limit=limit, sort=sort, timeframe=timeframe, session=session
                ),
            ),
            (
                "comments",
                lambda session: user.comments(
                    limit=limit, sort=sort, timeframe=timeframe, session=session
                ),
            ),
            (
                "moderated_communities",
                lambda session: user.moderated_communities(session=session),
            ),
            (
                "top_communities",
                lambda session: user.top_communities(
                    top_n=arguments.top_communities
                    if hasattr(arguments, "top_communities")
                    else None,
                    limit=limit,
                    sort=sort,
                    timeframe=timeframe,
                    session=session,
                ),
            ),
        ],
        "community": [
            ("profile", lambda session: community.profile(session=session)),
            (
                "posts",
                lambda session: community.posts(
                    limit=limit, sort=sort, timeframe=timeframe, session=session
                ),
            ),
        ],
        "posts": [
            (
                "front_page",
                lambda session: posts.front_page(
                    limit=limit, sort=sort, timeframe=timeframe, session=session
                ),
            ),
            (
                "search",
                lambda session: posts.search(
                    query=arguments.search,
                    limit=limit,
                    sort=sort,
                    timeframe=timeframe,
                    session=session,
                ),
            ),
            (
                "listing",
                lambda session: posts.listing(
                    listings_name=arguments.listing,
                    limit=limit,
                    sort=sort,
                    timeframe=timeframe,
                    session=session,
                ),
            ),
        ],
    }

    # ------------------------------------------------------------------------ #

    async with aiohttp.ClientSession() as request_session:
        # await get_updates(session=request_session)

        mode_action = function_mapping.get(arguments.mode)
        is_executed: bool = False

        for action, function in mode_action:
            if getattr(arguments, action, False):
                call_function = await function(session=request_session)

                # ------------------------------------------------------------- #

                target_directory: str = ""

                if arguments.csv or arguments.json:
                    target_directory = os.path.join(
                        PROGRAM_DIRECTORY, f"{arguments.mode}_{action}"
                    )
                    pathfinder(
                        directories=[
                            os.path.join(target_directory, "csv"),
                            os.path.join(target_directory, "json"),
                        ]
                    )

                # ------------------------------------------------------------- #

                if call_function:
                    rich.print(
                        dataframe(
                            data=call_function,
                            save_csv=arguments.csv,
                            save_json=arguments.json,
                            save_to_dir=target_directory,
                        )
                    )

                is_executed = True

                break

                # ------------------------------------------------------------- #

        if not is_executed:
            log.warning(
                f"knewkarma {arguments.mode}: missing one or more expected argument(s)."
            )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def run():
    """
    Main entrypoint for the Knew Karma command-line interface.
    """
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
        try:
            start_time: datetime = datetime.now()

            log.info(
                f"[bold]Knew Karma CLI[/] {version} started at "
                f"{start_time.strftime('%a %b %d %Y, %I:%M:%S%p')}..."
            )
            asyncio.run(stage_and_execute(arguments=arguments))
        except KeyboardInterrupt:
            log.warning(f"User interruption detected ([yellow]Ctrl+C[/])")
        finally:
            log.info(f"Stopped in {datetime.now() - start_time} seconds.")
    else:
        parser.print_usage()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
