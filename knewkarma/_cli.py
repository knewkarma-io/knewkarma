# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

import argparse
import asyncio
from datetime import datetime
from typing import Callable, Dict
from uuid import uuid4

import aiohttp
import rich
import yappi

from ._coreutils import log, save_data, pathfinder
from ._parser import create_parser, version
from .api import get_updates
from .base import RedditUser, RedditSub, RedditPosts


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def profiler(enable: bool, arguments: argparse):
    """
    Enables/Disables the profiler

    Parameters
    ----------
    enable: bool
        A boolean value indicating whether the profiler is enabled/disabled.
    arguments: argparse
        A Namespace object containing profiler options.
    """
    if arguments.has_been_run:
        if enable:
            yappi.set_clock_type(type=arguments.clock_type)
            yappi.start()
        else:
            yappi.stop()
            yappi.get_func_stats().sort(sort_type=arguments.stats_sort).print_all()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


async def setup_cli(
    cli_arguments: argparse.Namespace,
    argument_mapping: Dict[str, Dict[str, Callable]],
):
    # Create a custom Namespace object to store profiler options
    profiler_arguments = argparse.Namespace(
        has_been_run=cli_arguments.runtime_profiler,
        stats_sort=cli_arguments.prof_stats_sort,
        clock_type=cli_arguments.prof_clock_type,
    )

    if cli_arguments.mode in argument_mapping:
        mode_action = argument_mapping.get(cli_arguments.mode)

        for action_name, action_function in mode_action.items():
            if getattr(cli_arguments, action_name, False):
                profiler(enable=True, arguments=profiler_arguments)

                async with aiohttp.ClientSession() as session:
                    await get_updates(session=session)

                    function_data = (
                        await action_function(session=session)
                        if isinstance(await action_function(session=session), dict)
                        else [
                            data.__dict__
                            for data in await action_function(session=session)
                        ]
                    )

                    pathfinder()
                    save_data(
                        data=function_data,
                        filename=f"{uuid4()}_{cli_arguments.mode.upper()}_{action_name}",
                        save_to_json=cli_arguments.json,
                        save_to_csv=cli_arguments.csv,
                    )

                    rich.print(function_data)

                profiler(enable=False, arguments=profiler_arguments)
                break
        else:
            log.warning(
                f"knewkarma {cli_arguments.mode}: missing one or more expected argument(s)."
            )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def run_cli():
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
    argument_mapping: dict = {
        "user": {
            "profile": lambda session: user.profile(
                session=session,
            ),
            "posts": lambda session: user.posts(
                session=session,
            ),
            "comments": lambda session: user.comments(
                session=session,
            ),
        },
        "subreddit": {
            "profile": lambda session: subreddit.profile(
                session=session,
            ),
            "posts": lambda session: subreddit.posts(
                session=session,
            ),
        },
        "posts": {
            "front_page": lambda session: posts.front_page(
                session=session,
            ),
            "search": lambda session: posts.search(
                query=arguments.search,
                session=session,
            ),
            "listing": lambda session: posts.listing(
                listings_name=arguments.listing,
                session=session,
            ),
        },
    }

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
                f"{start_time.strftime('%a %b %d %Y, %I:%M:%S %p')}..."
            )
            asyncio.run(
                setup_cli(cli_arguments=arguments, argument_mapping=argument_mapping)
            )
        except KeyboardInterrupt:
            log.warning(f"User interruption detected ([yellow]Ctrl+C[/])")
        finally:
            log.info(f"Stopped in {datetime.now() - start_time} seconds.")
    else:
        parser.print_usage()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
