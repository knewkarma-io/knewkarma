import argparse
import asyncio
import os
from datetime import datetime
from typing import get_args

import aiohttp
from rich.markdown import Markdown
from rich.tree import Tree
from rich_argparse import RichHelpFormatter

from ._api import Api, DATA_TIMEFRAME, SORT_CRITERION, DATA_LISTING
from ._core import Post, Posts, Subreddit, Subreddits, User, Search
from ._utils import (
    console,
    pathfinder,
    systeminfo,
    export_dataframe,
    filename_timestamp,
    create_dataframe,
    show_exported_files,
)
from .docs import Docs
from .version import Version


def create_parser() -> argparse.ArgumentParser:
    """
    Creates and configures an argument parser for the command line arguments.

    :return: A configured argparse.ArgumentParser object ready to parse the command line arguments.
    :rtype: argparse.ArgumentParser
    """
    main_parser = argparse.ArgumentParser(
        description=Markdown(Docs.about, style="argparse.text"),
        epilog=Markdown(Docs.description),
        formatter_class=RichHelpFormatter,
    )
    subparsers = main_parser.add_subparsers(dest="module", help="module")
    main_parser.add_argument(
        "-t",
        "--timeframe",
        type=str,
        default="all",
        choices=list(get_args(DATA_TIMEFRAME)),
        help="([bold][green]bulk/semi-bulk[/][/]) timeframe to get data from (default: [green]%(default)s[/])",
    )
    main_parser.add_argument(
        "-s",
        "--sort",
        type=str,
        default="all",
        choices=list(get_args(SORT_CRITERION)),
        help="([bold][green]bulk/semi-bulk[/][/]) sort criterion (default: [green]%(default)s[/])",
    )
    main_parser.add_argument(
        "-l",
        "--limit",
        type=int,
        default=100,
        help="([bold][green]bulk/semi-bulk[/][/]) data output limit (default: [cyan]%(default)s[/])",
    )
    main_parser.add_argument(
        "--time-format",
        default="datetime",
        help="determines the format of the output time (default: [green]%(default)s[/])",
        choices=["concise", "datetime"],
    )
    main_parser.add_argument(
        "-e",
        "--export",
        type=str,
        help="a comma-separated list of file types to export the output to (supported: [green]csv,html,json,xml[/])",
    )
    main_parser.add_argument(
        "-u",
        "--updates",
        help="check for updates on run",
        action="store_true",
    )
    main_parser.add_argument(
        "-v",
        "--version",
        version=Markdown(f"Knew Karma {Version.release} {Docs.copyright}"),
        action="version",
    )

    post_parser = subparsers.add_parser(
        "post",
        help="post module ([bold][green]semi-bulk[/][/])",
        description=Markdown(
            "**Post Module**: *Pull an individual post's data*",
            style="argparse.text",
        ),
        epilog=Markdown(Docs.examples["post"]),
        formatter_class=RichHelpFormatter,
    )

    post_parser.add_argument("id", help="post id", type=str)
    post_parser.add_argument("subreddit", help="post source subreddit", type=str)
    post_parser.add_argument("-d", "--data", help="get post data", action="store_true")
    post_parser.add_argument(
        "-c", "--comments", help="get post comments", action="store_true"
    )

    posts_parser = subparsers.add_parser(
        "posts",
        help="posts module ([bold][green]bulk[/][/])",
        description=Markdown(
            "**Posts**: *Pull posts from various sources.*", style="argparse.text"
        ),
        epilog=Markdown(Docs.examples["posts"]),
        formatter_class=RichHelpFormatter,
    )
    posts_parser.add_argument(
        "-n",
        "--new",
        help="get new posts",
        action="store_true",
    )
    posts_parser.add_argument(
        "-f",
        "--front-page",
        help="get posts from the reddit front-page",
        action="store_true",
    )
    posts_parser.add_argument(
        "-l",
        "--listing",
        default="all",
        help="get posts from a specified listing",
        choices=list(get_args(DATA_LISTING)),
    )

    search_parser = subparsers.add_parser(
        "search",
        help="search module ([bold][green]bulk[/][/])",
        description=Markdown(
            "**Search**: *Get search results from various sources.*",
            style="argparse.text",
        ),
        epilog=Markdown(Docs.examples["search"]),
        formatter_class=RichHelpFormatter,
    )
    search_parser.add_argument("query", help="search query")
    search_parser.add_argument(
        "-u", "--users", help="search users", action="store_true"
    )
    search_parser.add_argument(
        "-p", "--posts", help="search posts", action="store_true"
    )
    search_parser.add_argument(
        "-s", "--subreddits", help="search subreddits", action="store_true"
    )

    subreddit_parser = subparsers.add_parser(
        "subreddit",
        help="subreddit module ([bold][green]semi-bulk[/][/])",
        description=Markdown(
            "**Subreddit**: *Pull a specified subreddit's data.*",
            style="argparse.text",
        ),
        epilog=Markdown(Docs.examples["subreddit"]),
        formatter_class=RichHelpFormatter,
    )
    subreddit_parser.add_argument(
        "subreddit",
        help="subreddit name",
    )
    subreddit_parser.add_argument(
        "-p",
        "--profile",
        help="get a subreddit's profile",
        action="store_true",
    )
    subreddit_parser.add_argument(
        "-s",
        "--search",
        help="get a subreddit's posts that contain the specified keyword",
        type=str,
    )
    subreddit_parser.add_argument(
        "-pp",
        "--posts",
        help="get a subreddit's posts",
        action="store_true",
    )
    subreddit_parser.add_argument(
        "-wp",
        "--wiki-page",
        dest="wiki_page",
        help="get a subreddit's specified wiki page data",
        metavar="WIKI_PAGE",
    )
    subreddit_parser.add_argument(
        "-wps",
        "--wiki-pages",
        dest="wiki_pages",
        help="get a subreddit's wiki pages",
        action="store_true",
    )

    subreddits_parser = subparsers.add_parser(
        "subreddits",
        help="subreddits module ([bold][green]bulk[/][/])",
        description=Markdown(
            "**Subreddits*: *Pull subreddits from various sources.*",
            style="argparse.text",
        ),
        epilog=Markdown(Docs.examples["subreddits"]),
        formatter_class=RichHelpFormatter,
    )
    subreddits_parser.add_argument(
        "-a",
        "--all",
        help="get all subreddits",
        action="store_true",
    )
    subreddits_parser.add_argument(
        "-d",
        "--default",
        help="get default subreddits",
        action="store_true",
    )
    subreddits_parser.add_argument(
        "-n",
        "--new",
        help="get new subreddits",
        action="store_true",
    )
    subreddits_parser.add_argument(
        "-p",
        "--popular",
        help="get popular subreddits",
        action="store_true",
    )

    user_parser = subparsers.add_parser(
        "user",
        help="user module ([bold][green]semi-bulk[/][/])",
        description=Markdown(
            "**User**: *Pull a specified user's data.*", style="argparse.text"
        ),
        epilog=Markdown(Docs.examples["user"]),
        formatter_class=RichHelpFormatter,
    )
    user_parser.add_argument("username", help="username")
    user_parser.add_argument(
        "-p",
        "--profile",
        help="get a user's profile",
        action="store_true",
    )
    user_parser.add_argument(
        "-c",
        "--comments",
        help="get a user's comments",
        action="store_true",
    )

    user_parser.add_argument(
        "-o",
        "--overview",
        help="get a user's most recent comment activity",
        action="store_true",
    )
    user_parser.add_argument(
        "-pp",
        "--posts",
        action="store_true",
        help="get a user's posts",
    )
    user_parser.add_argument(
        "-sp",
        "--search-posts",
        dest="search_posts",
        help="get a user's posts that contain the specified keyword",
        type=str,
    )
    user_parser.add_argument(
        "-sc",
        "--search-comments",
        dest="search_comments",
        help="get a user's comments that contain the specified keyword",
        type=str,
    )
    user_parser.add_argument(
        "-mc",
        "--moderated-subreddits",
        dest="moderated_subreddits",
        help="get subreddits moderated by the user",
        action="store_true",
    )
    user_parser.add_argument(
        "-tc",
        "--top-subreddits",
        dest="top_subreddits",
        metavar="TOP_N",
        type=int,
        help="get a user's top n subreddits based on subreddit frequency in n posts",
    )

    return main_parser


async def call_functions(args: argparse.Namespace, function_mapping: dict):
    """
    Calls command-line arguments' functions based on user-input.

    :param args: Argparse namespace object  containing parsed command-line arguments.
    :type args: argparse.Namespace
    :param function_mapping: Mapping of command-line commands to their respective functions
    :type function_mapping: dict
    """

    async with aiohttp.ClientSession() as request_session:
        if args.updates:
            await Api().get_updates(session=request_session)

        mode_action = function_mapping.get(args.module)
        directory: str = ""
        for action, function in mode_action:
            arg_is_present: bool = False
            if getattr(args, action, False):
                arg_is_present = True

                if args.export:
                    output_dir: str = os.path.expanduser(
                        os.path.join("~", "knewkarma-data")
                    )
                    # Create path to main directory in which target data files will be exported
                    directory = os.path.join(output_dir, args.module, action)

                    # Create file directories for supported data file types
                    pathfinder(
                        directories=[
                            os.path.join(directory, "csv"),
                            os.path.join(directory, "html"),
                            os.path.join(directory, "json"),
                            os.path.join(directory, "xml"),
                        ]
                    )

                function_data = await function(session=request_session)
                if function_data:
                    dataframe = create_dataframe(data=function_data)

                    # Print the DataFrame, excluding the 'raw_data' column if it exists
                    console.log(dataframe)

                    if args.export:
                        export_dataframe(
                            dataframe=dataframe,
                            filename=filename_timestamp(),
                            directory=directory,
                            formats=args.export.split(","),
                        )

                        # Show exported files
                        tree = Tree(
                            f":open_file_folder: [bold]{directory}[/]",
                            guide_style="bold bright_blue",
                        )
                        show_exported_files(tree=tree, directory=directory)
                        console.log(tree)

                break

        if not arg_is_present:
            console.log(
                f"knewkarma {args.module}: missing one or more expected argument(s)"
            )


def stage_and_start():
    """
    Main entrypoint for the Knew Karma command-line interface.
    """
    parser = create_parser()
    args: argparse = parser.parse_args()

    start_time: datetime = datetime.now()

    limit: int = args.limit
    sort = args.sort
    timeframe = args.timeframe
    time_format = args.time_format

    search_query = args.query if hasattr(args, "query") else None

    user = User(
        username=args.username if hasattr(args, "username") else None,
        time_format=time_format,
    )
    search = Search(time_format=time_format)
    subreddit = Subreddit(
        subreddit=args.subreddit if hasattr(args, "subreddit") else None,
        time_format=time_format,
    )
    subreddits = Subreddits(time_format=time_format)
    post = Post(
        post_id=args.id if hasattr(args, "id") else None,
        subreddit=args.subreddit if hasattr(args, "subreddit") else None,
        time_format=time_format,
    )
    posts = Posts(time_format=time_format)

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
                "moderated_subreddits",
                lambda session: user.moderated_subreddits(session=session),
            ),
            (
                "search_posts",
                lambda session: user.search_posts(
                    keyword=args.search_posts,
                    limit=limit,
                    sort=sort,
                    timeframe=timeframe,
                    session=session,
                ),
            ),
            (
                "search_comments",
                lambda session: user.search_comments(
                    keyword=args.search_comments,
                    limit=limit,
                    sort=sort,
                    timeframe=timeframe,
                    session=session,
                ),
            ),
            (
                "top_subreddits",
                lambda session: user.top_subreddits(
                    top_n=args.top_subreddits
                    if hasattr(args, "top_subreddits")
                    else None,
                    limit=limit,
                    sort=sort,
                    timeframe=timeframe,
                    session=session,
                ),
            ),
        ],
        "subreddit": [
            ("profile", lambda session: subreddit.profile(session=session)),
            (
                "posts",
                lambda session: subreddit.posts(
                    limit=limit, sort=sort, timeframe=timeframe, session=session
                ),
            ),
            (
                "search",
                lambda session: subreddit.search(
                    keyword=args.search,
                    limit=limit,
                    sort=sort,
                    timeframe=timeframe,
                    session=session,
                ),
            ),
            ("wiki_pages", lambda session: subreddit.wiki_pages(session=session)),
            (
                "wiki_page",
                lambda session: subreddit.wiki_page(
                    page=args.wiki_page if hasattr(args, "wiki_page") else None,
                    session=session,
                ),
            ),
        ],
        "subreddits": [
            ("all", lambda session: subreddits.all(limit=limit, session=session)),
            (
                "default",
                lambda session: subreddits.default(limit=limit, session=session),
            ),
            ("new", lambda session: subreddits.new(limit=limit, session=session)),
            (
                "popular",
                lambda session: subreddits.popular(limit=limit, session=session),
            ),
        ],
        "post": [
            ("profile", lambda session: post.profile(session=session)),
            (
                "comments",
                lambda session: post.comments(
                    limit=limit,
                    sort=sort,
                    session=session,
                ),
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
                    listings_name=args.listing,
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
                "subreddits",
                lambda session: search.subreddits(
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

    if args.module:
        print(
            """
┓┏┓         ┓┏┓
┃┫ ┏┓┏┓┓┏┏  ┃┫ ┏┓┏┓┏┳┓┏┓
┛┗┛┛┗┗ ┗┻┛  ┛┗┛┗┻┛ ┛┗┗┗┻"""
        )
        print(f"{'='*40}")
        with console.status(
            status=f"Working: [bold]Knew Karma (CLI) [cyan]{Version.release}[/][/]",
            spinner="dots2",
        ):
            for key, value in systeminfo().items():
                console.log(f"[green]◉[/] [bold]{key}[/]: {value}")

            print(f"{'='*40}")

            try:
                start_time: datetime = datetime.now()
                asyncio.run(
                    call_functions(args=args, function_mapping=function_mapping)
                )
            except KeyboardInterrupt:
                console.log(
                    "[yellow]✘[/] User interruption detected ([yellow]Ctrl+C[/])"
                )
            finally:
                elapsed_time = datetime.now() - start_time
                console.log(
                    f"[green]✔[/] Done! {elapsed_time.total_seconds():.2f} seconds elapsed."
                )
    else:
        parser.print_usage()
