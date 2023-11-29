# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

import argparse
import asyncio
from datetime import datetime
from typing import Union, Callable, Dict

import yappi

from . import api
from ._coreutils import log
from ._masonry import Masonry
from ._parser import create_parser, version


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
def setup_cli(
    cli_arguments: argparse,
    argument_mapping: Dict[str, Union[Callable, Dict[str, Callable]]],
):
    # Create a custom Namespace object to store profiler options
    profiler_arguments = argparse.Namespace(
        has_been_run=cli_arguments.runtime_profiler,
        stats_sort=cli_arguments.prof_stats_sort,
        clock_type=cli_arguments.prof_clock_type,
    )
    if cli_arguments.mode in argument_mapping:
        mode_action: Union[dict, Callable] = argument_mapping.get(cli_arguments.mode)

        call_function: callable = None

        if isinstance(mode_action, dict):
            for action_name, action_function in mode_action.items():
                if getattr(cli_arguments, action_name) and hasattr(
                    cli_arguments, action_name
                ):
                    call_function = action_function
                    break
                else:
                    log.warning(
                        f"knewkarma {cli_arguments.mode}: missing one or more expected argument(s): "
                        f"{list(mode_action.keys())}"
                    )
                    break
        elif callable(mode_action):
            call_function = mode_action
        else:
            log.critical(
                f"Unknown action type for {mode_action}: {type(mode_action).__name__}. "
                f"Expected Dict or Callable."
            )

        profiler(enable=True, arguments=profiler_arguments)
        asyncio.run(call_function())
        profiler(enable=False, arguments=profiler_arguments)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def run_cli():
    parser = create_parser()
    arguments: argparse = parser.parse_args()
    tree_masonry: Masonry = Masonry(api=api)

    data_limit: int = arguments.limit
    data_sorting: str = arguments.limit
    save_to_json: bool = arguments.json
    save_to_csv: bool = arguments.csv

    start_time: datetime = datetime.now()
    argument_mapping: dict = {
        "user": {
            "profile": lambda: tree_masonry.profile_tree(
                profile_type="user_profile",
                profile_source=arguments.username,
                save_to_json=save_to_json,
                save_to_csv=save_to_csv,
            ),
            "posts": lambda: tree_masonry.posts_tree(
                posts_type="user_posts",
                posts_source=arguments.username,
                limited_to=data_limit,
                sorted_by=data_sorting,
                save_to_json=save_to_json,
            ),
            "comments": lambda: tree_masonry.user_comments_tree(
                username=arguments.username,
                limited_to=data_limit,
                sorted_by=data_sorting,
                save_to_json=save_to_json,
            ),
        },
        "subreddit": {
            "profile": lambda: tree_masonry.profile_tree(
                profile_type="subreddit_profile",
                profile_source=arguments.subreddit,
                save_to_json=save_to_json,
                save_to_csv=save_to_csv,
            ),
            "posts": lambda: tree_masonry.posts_tree(
                posts_type="subreddit_posts",
                posts_source=arguments.subreddit,
                show_author=True,
                limited_to=data_limit,
                sorted_by=data_sorting,
                save_to_json=save_to_json,
            ),
        },
        "posts": {
            "front_page": lambda: tree_masonry.posts_tree(
                posts_type="front_page_posts",
                show_author=True,
                limited_to=data_limit,
                sorted_by=data_sorting,
                save_to_json=save_to_json,
            ),
            "listing": lambda: tree_masonry.posts_tree(
                posts_type="listing_posts",
                posts_source=arguments.listing,
                show_author=True,
                limited_to=data_limit,
                sorted_by=data_sorting,
                save_to_json=save_to_json,
            ),
        },
        "post": lambda: tree_masonry.post_data_tree(
            post_id=arguments.post_id,
            post_subreddit=arguments.post_subreddit,
            comments_limit=data_limit,
            comments_sort=data_sorting,
            save_to_json=save_to_json,
        ),
        "search": lambda: tree_masonry.posts_tree(
            posts_type="search_posts",
            posts_source=arguments.query,
            show_author=True,
            limited_to=data_limit,
            sorted_by=data_sorting,
            save_to_json=save_to_json,
        ),
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
            setup_cli(cli_arguments=arguments, argument_mapping=argument_mapping)
        except KeyboardInterrupt:
            log.warning(f"User interruption detected ([yellow]Ctrl+C[/])")
        finally:
            log.info(f"Stopped in {datetime.now() - start_time} seconds.")
    else:
        parser.print_usage()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
