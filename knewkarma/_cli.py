# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

import argparse
import asyncio
from datetime import datetime
from typing import Callable, Dict, Tuple

import aiohttp
import rich

from ._coreutils import log, save_data, pathfinder
from ._parser import create_parser, version
from .api import get_updates
from .base import RedditUser, RedditSub, RedditPosts


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


async def setup_cli(
    arguments: argparse.Namespace,
    function_mapping: Dict[str, Tuple[str, Callable]],
):
    mode_action = function_mapping.get(arguments.mode)
    is_executed: bool = False
    for action, function in mode_action:
        if getattr(arguments, action, False):
            async with aiohttp.ClientSession() as session:
                await get_updates(session=session)
                call_function = await function(session=session)

                rich.print(call_function)
                is_executed = True

                pathfinder()
                save_data(
                    data=call_function,
                    to_json=arguments.json,
                    to_csv=arguments.csv,
                )

    if not is_executed:
        log.warning(
            f"knewkarma {arguments.mode}: missing one or more expected argument(s)."
        )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def execute_cli():
    parser = create_parser()
    arguments: argparse = parser.parse_args()

    data_limit: int = arguments.limit
    data_sorting: str = arguments.limit

    user = RedditUser(
        username=arguments.username if hasattr(arguments, "username") else None,
        data_limit=data_limit,
        data_sort=data_sorting,
    )
    subreddit = RedditSub(
        subreddit=arguments.subreddit if hasattr(arguments, "subreddit") else None,
        data_limit=data_limit,
        data_sort=data_sorting,
    )
    posts = RedditPosts(limit=data_limit, sort=data_sorting)

    start_time: datetime = datetime.now()
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

    if arguments.mode:
        print(
            """
┓┏┓         ┓┏┓         
┃┫ ┏┓┏┓┓┏┏  ┃┫ ┏┓┏┓┏┳┓┏┓
┛┗┛┛┗┗ ┗┻┛  ┛┗┛┗┻┛ ┛┗┗┗┻"""
        )
        if arguments.mode in function_mapping:
            try:
                start_time: datetime = datetime.now()

                log.info(
                    f"[bold]Knew Karma CLI[/] {version} started at "
                    f"{start_time.strftime('%a %b %d %Y, %I:%M:%S %p')}..."
                )
                asyncio.run(
                    setup_cli(arguments=arguments, function_mapping=function_mapping)
                )
            except KeyboardInterrupt:
                log.warning(f"User interruption detected ([yellow]Ctrl+C[/])")
            finally:
                log.info(f"Stopped in {datetime.now() - start_time} seconds.")
    else:
        parser.print_usage()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
