# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

import argparse
import asyncio
import os
from datetime import datetime

import aiohttp

from . import RedditUser, RedditCommunity, RedditPosts
from ._api import get_updates
from ._parser import create_parser, version
from ._utils import log, pathfinder, dataframe
from .base import RedditSearch, RedditCommunities
from .info import PROGRAM_DIRECTORY


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


async def execute_functions(arguments: argparse.Namespace, function_mapping: dict):
    """
    Executes command-line arguments' functions based on user-input.

    :param arguments: Argparse namespace object  containing parsed command-line arguments.
    :type arguments: argparse.Namespace
    :param function_mapping: Mapping of command-line commands to their respective functions
    :type function_mapping: dict
    """

    async with aiohttp.ClientSession() as request_session:
        if arguments.updates:
            await get_updates(session=request_session)

        mode_action = function_mapping.get(arguments.mode)
        file_dir: str = ""
        for action, function in mode_action:
            arg_is_available: bool = False
            if getattr(arguments, action, False):
                arg_is_available = True
                # ------------------------------------------------------------ #

                if arguments.csv or arguments.json:
                    file_dir = os.path.join(PROGRAM_DIRECTORY, arguments.mode, action)
                    pathfinder(
                        directories=[
                            os.path.join(file_dir, "csv"),
                            os.path.join(file_dir, "json"),
                        ]
                    )

                # ----------------------------------------------------------- #

                function_data = await function(session=request_session)
                if function_data:
                    dataframe(
                        data=function_data,
                        save_csv=arguments.csv,
                        save_json=arguments.json,
                        to_dir=file_dir,
                    )
                break

        if not arg_is_available:
            log.warning(
                f"knewkarma {arguments.mode}: missing one or more expected argument(s)"
            )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def stage_and_start():
    """
    Main entrypoint for the Knew Karma command-line interface.
    """
    # ------------------------------------------------------------------------- #

    parser = create_parser()
    arguments: argparse = parser.parse_args()

    start_time: datetime = datetime.now()

    # ------------------------------------------------------------------------ #

    limit: int = arguments.limit
    sort = arguments.sort
    timeframe = arguments.timeframe

    search_query = arguments.query if hasattr(arguments, "query") else None

    # ------------------------------------------------------------------------ #

    user = RedditUser(
        username=arguments.username if hasattr(arguments, "username") else None,
    )
    search = RedditSearch()
    community = RedditCommunity(
        community=arguments.community if hasattr(arguments, "community") else None,
    )
    communities = RedditCommunities()
    posts = RedditPosts()

    # ------------------------------------------------------------------------ #

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
            ("overview", lambda session: user.overview(limit=limit, session=session)),
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
            ("wiki_pages", lambda session: community.wiki_pages(session=session)),
            (
                "wiki_page",
                lambda session: community.wiki_page(
                    page=arguments.wiki_page
                    if hasattr(arguments, "wiki_page")
                    else None,
                    session=session,
                ),
            ),
        ],
        "communities": [
            ("all", lambda session: communities.all(limit=limit, session=session)),
            (
                "default",
                lambda session: communities.default(limit=limit, session=session),
            ),
            ("new", lambda session: communities.new(limit=limit, session=session)),
            (
                "popular",
                lambda session: communities.popular(limit=limit, session=session),
            ),
        ],
        "posts": [
            ("new", lambda session: posts.new(limit=limit, sort=sort, session=session)),
            (
                "front_page",
                lambda session: posts.front_page(
                    limit=limit, sort=sort, timeframe=timeframe, session=session
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
        "search": [
            (
                "users",
                lambda session: search.users(
                    query=search_query, limit=limit, session=session
                ),
            ),
            (
                "communities",
                lambda session: search.communities(
                    query=search_query, limit=limit, session=session
                ),
            ),
            (
                "posts",
                lambda session: search.posts(
                    query=search_query,
                    limit=limit,
                    sort=sort,
                    timeframe=timeframe,
                    session=session,
                ),
            ),
        ],
    }

    # ------------------------------------------------------------------------ #

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
            asyncio.run(
                execute_functions(
                    arguments=arguments, function_mapping=function_mapping
                )
            )
        except KeyboardInterrupt:
            log.warning(f"User interruption detected ([yellow]Ctrl+C[/])")
        finally:
            log.info(f"Stopped in {datetime.now() - start_time} seconds.")
    else:
        parser.print_usage()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
